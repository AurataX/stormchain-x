import { health, type Health } from "@/lib/health";
import type { Graph } from "@/lib/types";

// Illustrative impact radius in metres per status; not a hazard model.
const RADIUS: Record<Health, number> = { failed: 2400, partial: 1700, unknown: 1300, operational: 900 };
// Stacked translucent discs give a soft region that is densest at the centre.
const LAYERS = [1, 0.75, 0.5, 0.28];
const css = (name: string) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

export function addZones(map: google.maps.Map, graph: Graph) {
  const discs = graph.assets.filter((a) => a.geometry.type === "Point").flatMap((asset) => {
    const [lng, lat] = asset.geometry.coordinates as number[];
    const tone = health(asset.type_id, graph.assessments[asset.id]);
    const weight = tone === "failed" ? 0.14 : 0.09;
    return LAYERS.map((scale) => new google.maps.Circle({
      map, center: { lat, lng }, radius: RADIUS[tone] * scale, clickable: false, zIndex: 0,
      fillColor: css(`--${tone}`), fillOpacity: weight, strokeWeight: 0,
    }));
  });
  return () => discs.forEach((disc) => disc.setMap(null));
}
