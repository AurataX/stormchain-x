import type * as maplibregl from "maplibre-gl";

const css = (name: string) =>
  getComputedStyle(document.documentElement).getPropertyValue(name).trim();

// Lines get line layers: a circle layer would draw rings at every road vertex.
export function addHighlights(map: maplibregl.Map) {
  const site = ["==", ["get", "kind"], "site"];
  const road = ["==", ["get", "kind"], "road"];
  const make = (id: string, color: string, radius: number, width: number, when: unknown[]) => {
    map.addLayer({ id: `${id}-road`, type: "line", source: "assets",
      filter: ["all", road, when] as never,
      layout: { "line-cap": "round" }, paint: { "line-color": color, "line-width": width } }, "roads");
    map.addLayer({ id: id, type: "circle", source: "assets",
      filter: ["all", site, when] as never,
      paint: { "circle-radius": radius, "circle-color": "transparent",
        "circle-stroke-color": color, "circle-stroke-width": 2 } });
  };
  make("planned", css("--brand"), 17, 10, ["==", ["get", "planned"], true]);
  make("selected", css("--text"), 13, 8, ["==", ["get", "id"], ""]);
}

export function select(map: maplibregl.Map, id: string | null) {
  for (const layer of ["selected", "selected-road"]) {
    map.setFilter(layer, [
      "all", ["==", ["get", "kind"], layer === "selected" ? "site" : "road"],
      ["==", ["get", "id"], id ?? ""],
    ] as never);
  }
}
