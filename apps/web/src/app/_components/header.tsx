import { useRef } from "react";
import { Database, TriangleAlert } from "lucide-react";

type Props = { asOf: string; onAsOf: (value: string) => void; planLabel: string; stale: boolean };

export function Header({ asOf, onAsOf, planLabel, stale }: Props) {
  const input = useRef<HTMLInputElement>(null);
  const latest = () => {
    if (input.current) input.current.value = "";
    onAsOf("");
  };
  return (
    <header className="bar">
      <strong>STORMCHAIN-X</strong>
      <span className="badge" title="Every observation is simulated; nothing here is live.">
        <Database size={16} strokeWidth={1.5} aria-hidden /> Synthetic data
      </span>
      <label className="inline">
        Evidence as of
        <input ref={input} type="datetime-local" defaultValue={asOf}
          onChange={(e) => e.target.value && onAsOf(e.target.value)}
          max={new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16)} />
      </label>
      {asOf && (
        <>
          <span className="muted" role="status">Showing evidence up to this time</span>
          <button className="link" onClick={latest}>Back to latest</button>
        </>
      )}
      <span>{planLabel}</span>
      {stale && (
        <span className="tone-partial">
          <TriangleAlert size={16} strokeWidth={1.5} aria-hidden /> Plan stale
        </span>
      )}
    </header>
  );
}
