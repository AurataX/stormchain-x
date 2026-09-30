"use client";
import { useMemo, useState } from "react";
import { post } from "@/lib/api";
import type { Plan } from "@/lib/plan-types";
import type { Graph, Scenario, Source } from "@/lib/types";
import { useApi } from "@/lib/use-api";

export const SCENARIO = "cyclone-demo";

export function useConsole() {
  const [asOf, setAsOfRaw] = useState("");
  const [selected, setSelected] = useState<string | null>(null);
  const [stale, setStale] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [refresh, setRefresh] = useState(0);
  const setAsOf = (value: string) => {
    setAsOfRaw(value);
    setStale(true);
  };
  const iso = asOf ? new Date(asOf).toISOString() : "";
  const at = iso ? `&as_of=${encodeURIComponent(iso)}` : "";
  const graph = useApi<Graph>(`/api/v1/infrastructure/graph?scenario_id=${SCENARIO}${at}`, refresh);
  const plans = useApi<Plan[]>(`/api/v1/recovery/plans?scenario_id=${SCENARIO}`, refresh);
  const scenario = useApi<Scenario>(`/api/v1/scenarios/${SCENARIO}`);
  const sources = useApi<Source[]>("/api/v1/observation-sources");
  const latest = plans.data?.[0];
  const planned = useMemo(() => new Set(latest?.plan_payload.actions.map((a) => a.id)), [latest]);

  async function generate() {
    setBusy(true);
    setError(null);
    try {
      await post("/api/v1/recovery/plans", { scenario_id: SCENARIO, ...(iso && { as_of: iso }) });
      setStale(false);
      setRefresh((n) => n + 1);
    } catch (e) {
      setError((e as Error).message);
    }
    setBusy(false);
  }

  const saved = () => {
    setStale(true);
    setRefresh((n) => n + 1);
  };
  return { asOf, setAsOf, selected, setSelected, stale, busy, error, refresh, graph, plans,
    scenario, sources, latest, planned, generate, saved };
}
