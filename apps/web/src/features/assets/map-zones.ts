import { health, type Health } from "@/lib/health";
import type { Graph } from "@/lib/types";

// Illustrative impact radius in metres per status; not a hazard model.
const RADIUS: Record<Health, number> = { failed: 2200, partial: 1600, unknown: 1200, operational: 900 };
const css = (name: string) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

export function addZones(map: google.maps.Map, graph: Graph) {
  const circles = graph.assets.filter((a) => a.geometry.type === "Point").map((asset) => {
    const [lng, lat] = asset.geometry.coordinates as number[];
    const tone = health(asset.type_id, graph.assessments[asset.id]);
    const color = css(`--${tone}`);
    return new google.maps.Circle({
      map, center: { lat, lng }, radius: RADIUS[tone], clickable: false, zIndex: 0,
      fillColor: color, fillOpacity: tone === "failed" ? 0.3 : 0.2,
      strokeColor: color, strokeOpacity: 0.7, strokeWeight: 2,
    });
  });
  return () => circles.forEach((circle) => circle.setMap(null));
}
