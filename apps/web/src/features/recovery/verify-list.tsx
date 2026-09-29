import type { Plan } from "@/lib/plan-types";

type Props = {
  items: Plan["plan_payload"]["verification_priority"];
  onSelect: (id: string) => void;
};

export function VerifyList({ items, onSelect }: Props) {
  return (
    <>
      <h3 title="Criticality × entropy. A heuristic, not formal value of information.">
        Verify next (heuristic)
      </h3>
      <ol>
        {items.slice(0, 5).map((item) => (
          <li key={item.asset_id}>
            <button className="link" onClick={() => onSelect(item.asset_id)}>{item.asset_id}</button>
            {" "}score {item.score.toFixed(2)}
          </li>
        ))}
      </ol>
    </>
  );
}
