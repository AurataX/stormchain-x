import { describe, health } from "@/lib/health";
import type { Graph } from "@/lib/types";

export function Situation({ graph }: { graph: Graph }) {
  const affected = graph.assets.filter((a) => health(a.type_id, graph.assessments[a.id]) === "failed");
  const unknown = graph.assets.filter((a) => health(a.type_id, graph.assessments[a.id]) === "unknown");
  return <section className="card stack" aria-label="Situation summary">
    <h2>What needs attention</h2>
    <p><strong>{affected.length}</strong> damaged assets or blocked roads.
      {" "}<strong>{unknown.length}</strong> assets still need verification.</p>
    <ul>{affected.map((asset) => <li key={asset.id}>
      {asset.name}: <span className="tone-failed">{describe(asset.type_id, "failed")}</span>
    </li>)}</ul>
    <p className="muted">Unknown does not mean failed. Select an asset to inspect reports and submit evidence.</p>
  </section>;
}
