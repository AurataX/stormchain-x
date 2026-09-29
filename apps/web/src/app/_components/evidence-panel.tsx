import { Inspector } from "@/features/assets/inspector";
import { EvidenceForm } from "@/features/observations/evidence-form";
import type { Action } from "@/lib/plan-types";
import type { Graph, Source } from "@/lib/types";
import { SCENARIO } from "./use-console";

type Props = {
  graph: Graph | null; selected: string | null; refresh: number;
  action?: Action; sources: Source[]; onSaved: () => void;
};

export function EvidencePanel({ graph, selected, refresh, action, sources, onSaved }: Props) {
  const asset = graph?.assets.find((a) => a.id === selected) ?? null;
  return (
    <>
      {graph && selected && (
        <Inspector id={selected} graph={graph} scenario={SCENARIO} refresh={refresh} action={action} />
      )}
      <EvidenceForm asset={asset} scenario={SCENARIO} sources={sources} onSaved={onSaved} />
    </>
  );
}
