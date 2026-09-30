import { money } from "@/lib/health";
import type { Scenario } from "@/lib/types";

export function Constraints({ scenario }: { scenario: Scenario | null }) {
  if (!scenario) return <p className="card">Loading scenario…</p>;
  return (
    <section aria-label="Scenario constraints" className="card constraints">
      <div>
        <h2>{scenario.name}</h2>
        <details><summary className="muted">Scenario assumptions · fixed constraints</summary>
          <p>{scenario.description}</p>
        </details>
      </div>
      <dl>
        <div><dt>Budget</dt><dd>{money(scenario.budget_cents)}</dd></div>
        <div><dt>Communications</dt><dd>{scenario.communication_mode.toLowerCase().replace("_", " ")}</dd></div>
        {Object.entries(scenario.available_crews).map(([crew, n]) => (
          <div key={crew}><dt>{crew} crews</dt><dd>{n}</dd></div>
        ))}
      </dl>
    </section>
  );
}
