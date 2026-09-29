const ITEMS = [
  ["operational", "Operational / open"],
  ["partial", "Partial"],
  ["failed", "Damaged, failed / blocked"],
  ["unknown", "Unknown (hollow marker)"],
] as const;

export function Legend() {
  return (
    <ul className="legend" aria-label="Map legend">
      {ITEMS.map(([tone, label]) => (
        <li key={tone}>
          <span className={`dot dot-${tone}`} aria-hidden /> {label}
        </li>
      ))}
      <li><span className="dot dot-plan" aria-hidden /> Planned repair</li>
      <li className="muted">Dashed line: dependency. Synthetic geometry, no basemap.</li>
    </ul>
  );
}
