import { health, money, type Health } from "@/lib/health";
import type { Plan } from "@/lib/plan-types";
import type { Graph, Scenario } from "@/lib/types";

type Props = { plan?: Plan; scenario: Scenario | null; graph: Graph | null; stale: boolean };
const TONES: [Health, string][] = [
  ["operational", "Operational"], ["partial", "Partial"], ["failed", "Damaged / blocked"], ["unknown", "Unknown"],
];

export function Kpis({ plan, scenario, graph, stale }: Props) {
  const solver = plan?.plan_payload.solver;
  const counts: Record<Health, number> = { operational: 0, partial: 0, failed: 0, unknown: 0 };
  graph?.assets.forEach((a) => counts[health(a.type_id, graph.assessments[a.id])]++);
  const share = plan && scenario ? Math.min(100, (plan.total_cost_cents / scenario.budget_cents) * 100) : 0;
  return (
    <div className="kpi-row">
      <article className="card kpi">
        <h2>Recovery plan</h2>
        <p className="kpi-value">{plan ? `v${plan.version}` : "None"}</p>
        <p className="muted">
          {solver ? `Solver ${solver.status}${solver.gap !== null ? `, gap ${(solver.gap * 100).toFixed(1)}%` : ""}` : "No plan yet"}
        </p>
        {stale && <span className="chip tone-partial">Stale: evidence changed</span>}
      </article>
      <article className="card kpi">
        <h2>Budget used</h2>
        <p className="kpi-value">{plan ? money(plan.total_cost_cents) : "—"}</p>
        <p className="muted">of {scenario ? money(scenario.budget_cents) : "—"}</p>
        <div className="bar-track" aria-hidden><div className="bar-fill" style={{ width: `${share}%` }} /></div>
      </article>
      <article className="card kpi">
        <h2>Total duration</h2>
        <p className="kpi-value">{plan ? `${plan.duration_minutes / 60} h` : "—"}</p>
        <p className="muted">{plan ? `${plan.plan_payload.actions.length} repairs scheduled` : "Generate a plan"}</p>
      </article>
      <article className="card kpi">
        <h2>Assets by status</h2>
        <ul className="counts">
          {TONES.map(([tone, label]) => (
            <li key={tone} className="chip">
              <span className={`dot dot-${tone}`} aria-hidden /> {counts[tone]} {label}
            </li>
          ))}
        </ul>
      </article>
    </div>
  );
}
