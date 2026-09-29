import { money } from "@/lib/health";
import type { Plan } from "@/lib/plan-types";

export function Compare({ current, previous }: { current: Plan; previous?: Plan }) {
  if (!previous) return <p>No earlier version to compare.</p>;
  const { diff } = current.deterministic_rationale;
  const rows: [string, string[]][] = [
    ["Added", diff.added], ["Removed", diff.removed], ["Rescheduled", diff.rescheduled],
  ];
  return (
    <table className="assets">
      <caption>Version {previous.version} → {current.version}</caption>
      <tbody>
        {rows.map(([label, ids]) => (
          <tr key={label}><th scope="row">{label}</th><td>{ids.join(", ") || "none"}</td></tr>
        ))}
        <tr>
          <th scope="row">Cost</th>
          <td>{money(previous.total_cost_cents)} → {money(current.total_cost_cents)}</td>
        </tr>
        <tr>
          <th scope="row">Duration</th>
          <td>{previous.duration_minutes / 60} h → {current.duration_minutes / 60} h</td>
        </tr>
      </tbody>
    </table>
  );
}
