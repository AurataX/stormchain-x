import type * as maplibregl from "maplibre-gl";

export const css = (name: string) =>
  getComputedStyle(document.documentElement).getPropertyValue(name).trim();

export function baseStyle(): maplibregl.StyleSpecification {
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  const tiles = ["a", "b", "c"].map(
    (host) => `https://${host}.basemaps.cartocdn.com/${dark ? "dark_all" : "light_all"}/{z}/{x}/{y}.png`,
  );
  const basemap = { type: "raster" as const, tiles, tileSize: 256, maxzoom: 19,
    attribution: "© OpenStreetMap contributors © CARTO" };
  return {
    version: 8,
    sources: { basemap },
    layers: [
      { id: "bg", type: "background", paint: { "background-color": css("--canvas") } },
      { id: "basemap", type: "raster", source: "basemap", paint: { "raster-opacity": 0.85 } },
    ],
  };
}

export function watchBasemap(map: maplibregl.Map, onDown: () => void) {
  map.on("error", (event) => {
    if ((event as { sourceId?: string }).sourceId === "basemap") onDown();
  });
}
