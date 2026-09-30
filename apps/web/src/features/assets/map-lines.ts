import { mapData } from "./map-data";
import type { Graph } from "@/lib/types";

const css = (name: string) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

export function addLines(map: google.maps.Map, graph: Graph, planned: Set<string>,
  selected: string | null, onSelect: (id: string) => void) {
  const data = mapData(graph, planned);
  const links = data.links.features.map((feature) => {
    const coordinates = (feature.geometry as { coordinates: number[][] }).coordinates;
    return new google.maps.Polyline({ map, clickable: false, strokeOpacity: 0,
      path: coordinates.map(([lng, lat]) => ({ lat, lng })),
      icons: [{ icon: { path: "M 0,-1 0,1", strokeColor: css("--text-2"), strokeOpacity: 0.7, scale: 2 }, repeat: "12px" }],
    });
  });
  const roads = data.assets.features.filter((f) => f.geometry.type === "LineString").flatMap((feature) => {
    const properties = feature.properties!;
    const coordinates = (feature.geometry as { coordinates: number[][] }).coordinates;
    const path = coordinates.map(([lng, lat]) => ({ lat, lng }));
    const highlighted = properties.id === selected || properties.planned;
    const glow = new google.maps.Polyline({ map, path, strokeWeight: 12, clickable: false, zIndex: 0,
      strokeColor: css(`--${properties.health}`), strokeOpacity: 0.3 });
    const layers = highlighted ? [glow, new google.maps.Polyline({ map, path, strokeWeight: 10,
      strokeColor: css(properties.id === selected ? "--text" : "--brand"), zIndex: 1 })] : [glow];
    const road = new google.maps.Polyline({ map, path, strokeWeight: 4,
      strokeColor: css(`--${properties.health}`), zIndex: 2 });
    road.addListener("click", () => onSelect(String(properties.id)));
    return [...layers, road];
  });
  return () => [...links, ...roads].forEach((line) => {
    google.maps.event.clearInstanceListeners(line);
    line.setMap(null);
  });
}
