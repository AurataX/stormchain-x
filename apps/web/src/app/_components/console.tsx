"use client";
import { useState } from "react";
import { AssetMap } from "@/features/assets/map";
import { Legend } from "@/features/assets/legend";
import { AssetTable } from "@/features/assets/asset-table";
import { Inspector } from "@/features/assets/inspector";
import { EvidenceForm } from "@/features/observations/evidence-form";
import { PlanPanel } from "@/features/recovery/plan-panel";
import { Constraints } from "./constraints";
import { Header } from "./header";
import { SCENARIO, useConsole } from "./use-console";

const TABS = ["map", "plan", "evidence"] as const;

export function Console() {
  const c = useConsole();
  const [tab, setTab] = useState<(typeof TABS)[number]>("map");
  const graph = c.graph.data;
  const asset = graph?.assets.find((a) => a.id === c.selected) ?? null;
  return (
    <div className="console" data-tab={tab}>
      <Header asOf={c.asOf} onAsOf={c.setAsOf} stale={c.stale}
        planLabel={c.latest ? `Plan v${c.latest.version}` : "No plan yet"} />
      <nav className="tabs" role="tablist" aria-label="Views">
        {TABS.map((name) => (
          <button key={name} role="tab" aria-selected={tab === name} onClick={() => setTab(name)}>{name}</button>
        ))}
      </nav>
      {c.graph.error && (
        <p className="banner tone-failed" role="alert">
          Disconnected: {c.graph.error} <button className="link" onClick={c.graph.reload}>Retry</button>
        </p>
      )}
      <main>
        <div className="panel mapbox" data-panel="map">
          {graph ? (
            <>
              <AssetMap graph={graph} planned={c.planned} selected={c.selected} onSelect={c.setSelected} />
              <Legend />
            </>
          ) : (
            <div className="map card">{c.graph.loading ? "Loading map…" : "Map unavailable."}</div>
          )}
        </div>
        <aside className="panel rail" data-panel="map">
          <Constraints scenario={c.scenario.data} />
          {graph && <AssetTable graph={graph} selected={c.selected} onSelect={c.setSelected} />}
        </aside>
        <div className="panel evidence" data-panel="evidence">
          {graph && c.selected && (
            <Inspector id={c.selected} graph={graph} scenario={SCENARIO} refresh={c.refresh}
              action={c.latest?.plan_payload.actions.find((a) => a.id === c.selected)} />
          )}
          <EvidenceForm asset={asset} scenario={SCENARIO} sources={c.sources.data ?? []} onSaved={c.saved} />
        </div>
        <div className="panel plan" data-panel="plan">
          <PlanPanel plans={c.plans.data ?? []} scenario={c.scenario.data} stale={c.stale}
            busy={c.busy} error={c.error ?? c.plans.error} onGenerate={c.generate} onSelect={c.setSelected} />
        </div>
      </main>
    </div>
  );
}
