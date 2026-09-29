import type * as maplibregl from "maplibre-gl";
import { addHighlights } from "./map-highlight";
import { css } from "./map-style";

export function addLayers(map: maplibregl.Map) {
  const [ok, part, bad, unknown] = ["--operational", "--partial", "--failed", "--unknown"].map(css);
  const health = ["match", ["get", "health"], "operational", ok, "partial", part, "failed", bad, unknown];
  const empty = { type: "FeatureCollection" as const, features: [] };
  map.addSource("links", { type: "geojson", data: empty });
  map.addSource("assets", { type: "geojson", data: empty, promoteId: "id" });
  map.addLayer({ id: "links", type: "line", source: "links",
    paint: { "line-color": css("--text-2"), "line-width": 1, "line-dasharray": [2, 3] } });
  map.addLayer({ id: "roads", type: "line", source: "assets",
    filter: ["==", ["get", "kind"], "road"],
    paint: { "line-color": health as never, "line-width": 4 } });
  map.addLayer({ id: "sites", type: "circle", source: "assets",
    filter: ["==", ["get", "kind"], "site"],
    paint: {
      "circle-radius": 9,
      "circle-color": ["match", ["get", "health"], "unknown", "transparent", health] as never,
      "circle-stroke-color": ["match", ["get", "health"], "unknown", unknown, css("--surface")] as never,
      "circle-stroke-width": ["match", ["get", "health"], "unknown", 3, 2] as never,
    } });
  addHighlights(map);
}
