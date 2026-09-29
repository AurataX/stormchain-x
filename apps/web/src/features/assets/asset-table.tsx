import { describe, health } from "@/lib/health";
import type { Graph } from "@/lib/types";

type Props = { graph: Graph; selected: string | null; onSelect: (id: string) => void };

export function AssetTable({ graph, selected, onSelect }: Props) {
  return (
    <section className="card" aria-label="Assets">
      <table className="assets">
        <caption>Assets (keyboard alternative to the map)</caption>
        <thead>
          <tr><th>Asset</th><th>Status</th></tr>
        </thead>
        <tbody>
          {graph.assets.map((asset) => {
            const value = health(asset.type_id, graph.assessments[asset.id]);
            return (
              <tr key={asset.id} aria-selected={asset.id === selected}>
                <td>
                  <button className="link" onClick={() => onSelect(asset.id)}>{asset.name}</button>
                </td>
                <td>
                  <span className={`chip tone-${value}`}>
                    <span className={`dot dot-${value}`} aria-hidden />
                    {describe(asset.type_id, value)}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </section>
  );
}
