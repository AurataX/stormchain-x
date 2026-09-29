import { money } from "@/lib/health";
import type { Plan } from "@/lib/plan-types";
import type { Scenario } from "@/lib/types";
import { ActionsTable } from "./actions-table";
import { Compare } from "./compare";
import { VerifyList } from "./verify-list";

type Props = {
  plans: Plan[]; scenario: Scenario | null; stale: boolean; busy: boolean;
  error: string | null; onGenerate: () => void; onSelect: (id: string) => void;
};

export function PlanPanel({ plans, scenario, stale, busy, error, onGenerate, onSelect }: Props) {
  const plan = plans[0];
  const solver = plan?.plan_payload.solver;
  return (
    <section aria-label="Recovery plan" className="card stack">
      <div className="row">
        <h2>{plan ? `Plan v${plan.version}` : "Recovery plan"}</h2>
        <button className="primary" onClick={onGenerate} disabled={busy}>
          {busy ? "Solving…" : plan ? "Recalculate" : "Generate plan"}
        </button>
      </div>
      {stale && <p className="tone-partial" role="status">Stale: evidence changed since this plan.</p>}
      {error && <p className="tone-failed" role="alert">{error}</p>}
      {!plan && !error && <p>No plan yet. Generate one from current evidence.</p>}
      {plan && solver && (
        <>
          <p className="muted">
            Solver {solver.status}
            {solver.status !== "OPTIMAL" && " (not proven optimal)"}
            {solver.gap !== null && `, gap ${(solver.gap * 100).toFixed(1)}%`}
            {" · "}{money(plan.total_cost_cents)} of {scenario ? money(scenario.budget_cents) : "—"} budget,{" "}
            {plan.duration_minutes / 60} h total
          </p>
          <ActionsTable actions={plan.plan_payload.actions} onSelect={onSelect} />
          <VerifyList items={plan.plan_payload.verification_priority} onSelect={onSelect} />
          <details>
            <summary>Compare with previous version</summary>
            <Compare current={plan} previous={plans[1]} />
          </details>
          <details>
            <summary>Assumptions</summary>
            <ul>{plan.plan_payload.assumptions.map((t) => <li key={t}>{t}</li>)}</ul>
          </details>
        </>
      )}
    </section>
  );
}
