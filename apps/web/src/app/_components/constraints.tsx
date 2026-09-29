import { money } from "@/lib/health";
import type { Scenario } from "@/lib/types";

export function Constraints({ scenario }: { scenario: Scenario | null }) {
  if (!scenario) return <p className="card">Loading scenario…</p>;
  return (
    <section aria-label="Scenario constraints" className="card">
      <h2>{scenario.name}</h2>
      <p>{scenario.description}</p>
      <dl>
        <dt>Budget</dt><dd>{money(scenario.budget_cents)}</dd>
        <dt>Communications</dt><dd>{scenario.communication_mode.toLowerCase().replace("_", " ")}</dd>
        {Object.entries(scenario.available_crews).map(([crew, n]) => (
          <div key={crew}><dt>{crew} crews</dt><dd>{n}</dd></div>
        ))}
      </dl>
      <p className="muted">Constraints are read-only: the API has no scenario editing.</p>
    </section>
  );
}
