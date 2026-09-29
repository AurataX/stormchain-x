"use client";
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef, useState } from "react";
import type { Graph } from "@/lib/types";
import { bounds, mapData } from "./map-data";
import { select } from "./map-highlight";
import { addLayers } from "./map-layers";
import { baseStyle, watchBasemap } from "./map-style";

maplibregl.setWorkerUrl("/maplibre/maplibre-gl-worker.mjs");

type Props = {
  graph: Graph;
  planned: Set<string>;
  selected: string | null;
  onSelect: (id: string) => void;
};

export function AssetMap({ graph, planned, selected, onSelect }: Props) {
  const box = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const pick = useRef(onSelect);
  pick.current = onSelect;
  const [ready, setReady] = useState(false);
  const fitted = useRef(false);
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    const m = new maplibregl.Map({
      container: box.current!, center: [83.315, 17.76], zoom: 11.6,
      attributionControl: { compact: true }, style: baseStyle(),
    });
    map.current = m;
    watchBasemap(m, () => setOffline(true));
    m.on("load", () => {
      addLayers(m);
      m.on("click", (event) => {
        const hit = m.queryRenderedFeatures(event.point, { layers: ["sites", "roads"] })[0];
        if (hit) pick.current(String(hit.properties.id));
      });
      setReady(true);
    });
    return () => m.remove();
  }, []);

  useEffect(() => {
    const m = map.current;
    if (!m || !ready) return;
    const data = mapData(graph, planned);
    (m.getSource("assets") as maplibregl.GeoJSONSource).setData(data.assets);
    (m.getSource("links") as maplibregl.GeoJSONSource).setData(data.links);
    select(m, selected);
    if (!fitted.current) {
      m.fitBounds(bounds(graph), { padding: 60, duration: 0 });
      fitted.current = true;
    }
  }, [graph, planned, selected, ready]);

  return (
    <>
      <div ref={box} className="map" role="application"
        aria-label="Asset map of synthetic geometry. Use the asset list for keyboard access." />
      {offline && <p className="basemap-note" role="status">Basemap unavailable; showing synthetic geometry only.</p>}
    </>
  );
}
