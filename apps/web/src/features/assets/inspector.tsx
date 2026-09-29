import { ago, describe, health } from "@/lib/health";
import type { Action } from "@/lib/plan-types";
import type { AssetDetail, Graph } from "@/lib/types";
import { useApi } from "@/lib/use-api";

type Props = { id: string; graph: Graph; scenario: string; action?: Action; refresh: number };

export function Inspector({ id, graph, scenario, action, refresh }: Props) {
  const asset = graph.assets.find((item) => item.id === id);
  const detail = useApi<AssetDetail>(`/api/v1/assets/${id}?scenario_id=${scenario}`, refresh);
  if (!asset) return null;
  const assessment = graph.assessments[id];
  const value = health(asset.type_id, assessment);
  const last = detail.data?.observations[0];
  return (
    <section aria-label="Asset inspector" className="card">
      <h2>{asset.name}</h2>
      <p className={`tone-${value}`}>{describe(asset.type_id, value)}</p>
      <p>
        {detail.loading && !last ? "Loading reports…" : detail.error ? `Reports unavailable: ${detail.error}`
          : last ? `Last report: ${ago(last.recorded_at)} from ${last.source_id}` : "No reports yet"}
      </p>
      <p title="Modeled route from a depot; uncertain evidence stays UNKNOWN.">
        Route access: {graph.access[id]?.toLowerCase()}
      </p>
      {assessment.flags.length > 0 && <p>Flags: {assessment.flags.join(", ")}</p>}
      {action && (
        <p>Planned repair: hour {action.start_hour}–{action.end_hour}, {action.crew_type} crew</p>
      )}
      <ul>
        {(detail.data?.dependencies ?? []).map((edge) => (
          <li key={edge.id}>{edge.source_asset_id} → {edge.target_asset_id} ({edge.dependency_type})</li>
        ))}
      </ul>
    </section>
  );
}
