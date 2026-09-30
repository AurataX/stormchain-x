"use client";
import { useState } from "react";
import { AssetMap } from "@/features/assets/map";
import { Legend } from "@/features/assets/legend";
import { AssetTable } from "@/features/assets/asset-table";
import { PlanPanel } from "@/features/recovery/plan-panel";
import { Constraints } from "./constraints";
import { Header } from "./header";
import { Kpis } from "./kpis";
import { EvidencePanel } from "./evidence-panel";
import { Tabs, type Tab } from "./tabs";
import { useConsole } from "./use-console";

export function Console() {
  const c = useConsole();
  const [tab, setTab] = useState<Tab>("map");
  const graph = c.graph.data;
  return (
    <div className="console" data-tab={tab}>
      <Header asOf={c.asOf} onAsOf={c.setAsOf} stale={c.stale && !!c.latest}
        planLabel={c.latest ? `Plan v${c.latest.version}` : "No plan yet"} />
      <Tabs tab={tab} onTab={setTab} />
      {c.graph.error && (
        <p className="banner tone-failed" role="alert">
          Disconnected: {c.graph.error} <button className="link" onClick={c.graph.reload}>Retry</button>
        </p>
      )}
      <main>
        <div className="panel kpis" data-panel="map">
          <Kpis plan={c.latest} scenario={c.scenario.data} graph={graph} stale={c.stale} />
        </div>
        <div className="panel mapbox" data-panel="map">
          <h2>Infrastructure impact <span className="muted">Select an asset to inspect evidence</span></h2>
          {graph ? (
            <>
              <AssetMap graph={graph} planned={c.planned} selected={c.selected} onSelect={c.setSelected} />
              <Legend />
            </>
          ) : (
            <div className="map card">{c.graph.loading ? "Loading map…" : "Map unavailable."}</div>
          )}
        </div>
        <div className="panel assets" data-panel="map">
          {graph && <AssetTable graph={graph} selected={c.selected} onSelect={c.setSelected} />}
        </div>
        <div className="panel scenario" data-panel="map">
          <Constraints scenario={c.scenario.data} />
        </div>
        <div className="panel evidence" data-panel="evidence">
          <EvidencePanel graph={graph} selected={c.selected} refresh={c.refresh} onSaved={c.saved}
            sources={c.sources.data ?? []}
            action={c.latest?.plan_payload.actions.find((x) => x.id === c.selected)} />
        </div>
        <div className="panel plan" data-panel="plan">
          <PlanPanel plans={c.plans.data ?? []} scenario={c.scenario.data} stale={c.stale}
            busy={c.busy} error={c.error ?? c.plans.error} onGenerate={c.generate}
            onSelect={c.setSelected} selected={c.selected} />
        </div>
      </main>
    </div>
  );
}
