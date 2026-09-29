import type { Plan } from "@/lib/plan-types";

type Props = {
  items: Plan["plan_payload"]["verification_priority"];
  onSelect: (id: string) => void;
};

export function VerifyList({ items, onSelect }: Props) {
  const top = items.slice(0, 5);
  const max = Math.max(...top.map((item) => item.score), 1);
  return (
    <table className="assets" title="Criticality × entropy. A heuristic, not formal value of information.">
      <caption>Verify next (heuristic)</caption>
      <thead>
        <tr><th>#</th><th>Asset</th><th>Score</th></tr>
      </thead>
      <tbody>
        {top.map((item, index) => (
          <tr key={item.asset_id}>
            <td>{index + 1}</td>
            <td><button className="link" onClick={() => onSelect(item.asset_id)}>{item.asset_id}</button></td>
            <td>
              <span>{item.score.toFixed(2)}</span>
              <div className="bar-track" aria-hidden>
                <div className="bar-fill" style={{ width: `${(item.score / max) * 100}%` }} />
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
