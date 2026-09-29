import { money } from "@/lib/health";
import type { Action } from "@/lib/plan-types";

type Props = { actions: Action[]; onSelect: (id: string) => void };

export function ActionsTable({ actions, onSelect }: Props) {
  if (actions.length === 0) return <p>No repairs selected under current evidence.</p>;
  return (
    <table className="assets">
      <caption>Repair schedule</caption>
      <thead>
        <tr><th>#</th><th>Asset</th><th>Window</th><th>Crew</th><th>Cost</th></tr>
      </thead>
      <tbody>
        {actions.map((a, index) => (
          <tr key={a.id}>
            <td>{index + 1}</td>
            <td><button className="link" onClick={() => onSelect(a.id)}>{a.id}</button></td>
            <td>h{a.start_hour}–{a.end_hour}</td>
            <td>{a.crew_type}</td>
            <td>{money(a.cost_cents)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
