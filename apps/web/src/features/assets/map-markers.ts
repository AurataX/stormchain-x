import { health } from "@/lib/health";
import type { Graph } from "@/lib/types";

export function addMarkers(map: google.maps.Map, graph: Graph, planned: Set<string>,
  selected: string | null, onSelect: (id: string) => void) {
  const markers = graph.assets.filter((a) => a.geometry.type === "Point").map((asset) => {
    const [lng, lat] = asset.geometry.coordinates as number[];
    const tone = health(asset.type_id, graph.assessments[asset.id]);
    const dot = document.createElement("span");
    dot.className = `map-marker dot-${tone}${planned.has(asset.id) ? " is-planned" : ""}${selected === asset.id ? " is-selected" : ""}`;
    dot.textContent = tone === "unknown" ? "?" : "";
    const marker = new google.maps.marker.AdvancedMarkerElement({
      map, position: { lat, lng }, title: `${asset.name}: ${tone}`, gmpClickable: true,
      zIndex: selected === asset.id ? 2 : 1,
    });
    marker.append(dot);
    const pick = () => onSelect(asset.id);
    marker.addEventListener("gmp-click", pick);
    return { marker, pick };
  });
  return () => markers.forEach(({ marker, pick }) => {
    marker.removeEventListener("gmp-click", pick);
    marker.map = null;
  });
}
