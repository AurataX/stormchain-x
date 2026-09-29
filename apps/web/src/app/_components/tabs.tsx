export const TABS = [["map", "Overview"], ["plan", "Plan"], ["evidence", "Evidence"]] as const;
export type Tab = (typeof TABS)[number][0];

export function Tabs({ tab, onTab }: { tab: Tab; onTab: (tab: Tab) => void }) {
  return (
    <nav className="tabs" role="tablist" aria-label="Views">
      {TABS.map(([name, label]) => (
        <button key={name} role="tab" aria-selected={tab === name} onClick={() => onTab(name)}>
          {label}
        </button>
      ))}
    </nav>
  );
}
