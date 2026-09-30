"use client";
import { useEffect, useRef, useState } from "react";
import type { Graph } from "@/lib/types";
import { loadGoogleMaps } from "./google-loader";
import { bounds } from "./map-data";
import { addMarkers } from "./map-markers";
import { addLines } from "./map-lines";

type Props = { graph: Graph; planned: Set<string>; selected: string | null; onSelect: (id: string) => void };

export function AssetMap({ graph, planned, selected, onSelect }: Props) {
  const box = useRef<HTMLDivElement>(null);
  const [map, setMap] = useState<google.maps.Map>();
  const [error, setError] = useState("");
  const fitted = useRef(false);
  useEffect(() => {
    let active = true;
    const fail = () => setError("Google Maps authorization failed. Use the asset list below.");
    window.addEventListener("stormchain-map-error", fail);
    loadGoogleMaps().then(() => {
      if (active) setMap(new google.maps.Map(box.current!, {
        mapId: process.env.NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID || "DEMO_MAP_ID",
        center: { lat: 17.76, lng: 83.315 }, zoom: 11,
        colorScheme: google.maps.ColorScheme.FOLLOW_SYSTEM,
        mapTypeControl: false, streetViewControl: false, fullscreenControl: false,
        gestureHandling: "cooperative",
      }));
    }).catch((e: Error) => { if (active) setError(e.message); });
    return () => { active = false; window.removeEventListener("stormchain-map-error", fail); };
  }, []);
  useEffect(() => {
    if (!map) return;
    const clearMarkers = addMarkers(map, graph, planned, selected, onSelect);
    const clearLines = addLines(map, graph, planned, selected, onSelect);
    if (!fitted.current && graph.assets.length) {
      const [sw, ne] = bounds(graph);
      map.fitBounds({ west: sw[0], south: sw[1], east: ne[0], north: ne[1] }, 40);
      fitted.current = true;
    }
    return () => { clearMarkers(); clearLines(); };
  }, [map, graph, planned, selected, onSelect]);
  return <>
    <div ref={box} className="map" aria-label="Infrastructure map; keyboard alternative below." />
    {(!map || error) && <p className="basemap-note" role={error ? "alert" : "status"}>{error || "Loading Google Maps…"}</p>}
  </>;
}
