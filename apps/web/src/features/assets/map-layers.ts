import type { Graph } from "@/lib/types";
import { addLines } from "./map-lines";
import { addMarkers } from "./map-markers";
import { addZones } from "./map-zones";

export function addLayers(map: google.maps.Map, graph: Graph, planned: Set<string>,
  selected: string | null, onSelect: (id: string) => void) {
  const clear = [
    addZones(map, graph),
    addLines(map, graph, planned, selected, onSelect),
    addMarkers(map, graph, planned, selected, onSelect),
  ];
  return () => clear.forEach((fn) => fn());
}
