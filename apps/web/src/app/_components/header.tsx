import { Database, TriangleAlert } from "lucide-react";

type Props = { asOf: string; onAsOf: (value: string) => void; planLabel: string; stale: boolean };

export function Header({ asOf, onAsOf, planLabel, stale }: Props) {
  return (
    <header className="bar">
      <strong>STORMCHAIN-X</strong>
      <span className="badge" title="Every observation is simulated; nothing here is live.">
        <Database size={16} strokeWidth={1.5} aria-hidden /> Synthetic data
      </span>
      <label className="inline">
        Evidence as of
        <input type="datetime-local" value={asOf} onChange={(e) => onAsOf(e.target.value)}
          max={new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16)} />
      </label>
      {asOf && <button className="link" onClick={() => onAsOf("")}>Use now</button>}
      <span>{planLabel}</span>
      {stale && (
        <span className="tone-partial">
          <TriangleAlert size={16} strokeWidth={1.5} aria-hidden /> Plan stale
        </span>
      )}
    </header>
  );
}
