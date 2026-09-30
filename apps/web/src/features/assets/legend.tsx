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
      <li><span className="dot dot-plan" aria-hidden /> Blue dot: planned repair</li>
      <li className="muted">Shaded circle: impact zone by status · Glowing line: road · Dashed: dependency · Synthetic locations</li>
    </ul>
  );
}

const ZONES = [
  ["failed", "High impact"],
  ["partial", "Partial"],
  ["unknown", "Unverified"],
  ["operational", "Clear"],
] as const;

export function MapKey() {
  return (
    <div className="map-key" aria-hidden>
      <strong>Impact zones</strong>
      {ZONES.map(([tone, label]) => (
        <span key={tone}><i className={`zone zone-${tone}`} /> {label}</span>
      ))}
    </div>
  );
}
