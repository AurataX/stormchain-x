import type { Feature, FeatureCollection, Geometry } from "geojson";
import { health } from "@/lib/health";
import type { Graph } from "@/lib/types";

type Row = Feature<Geometry, Record<string, string | boolean>>;

export function mapData(graph: Graph, planned: Set<string>) {
  const point = new Map(
    graph.assets
      .filter((asset) => asset.geometry.type === "Point")
      .map((asset) => [asset.id, asset.geometry.coordinates as number[]]),
  );
  const assets: Row[] = graph.assets.map((asset) => ({
    type: "Feature",
    geometry: asset.geometry as Geometry,
    properties: {
      id: asset.id,
      kind: asset.geometry.type === "Point" ? "site" : "road",
      health: health(asset.type_id, graph.assessments[asset.id]),
      planned: planned.has(asset.id),
    },
  }));
  const links: Row[] = graph.dependencies.flatMap((edge) => {
    const from = point.get(edge.source_asset_id);
    const to = point.get(edge.target_asset_id);
    if (!from || !to) return [];
    return [{
      type: "Feature",
      geometry: { type: "LineString", coordinates: [from, to] },
      properties: { id: edge.id, kind: edge.dependency_type },
    }];
  });
  return {
    assets: { type: "FeatureCollection", features: assets } as FeatureCollection,
    links: { type: "FeatureCollection", features: links } as FeatureCollection,
  };
}

export function bounds(graph: Graph): [[number, number], [number, number]] {
  const points = graph.assets.flatMap((asset) =>
    asset.geometry.type === "Point"
      ? [asset.geometry.coordinates as number[]]
      : (asset.geometry.coordinates as number[][]),
  );
  const xs = points.map((p) => p[0]);
  const ys = points.map((p) => p[1]);
  return [[Math.min(...xs), Math.min(...ys)], [Math.max(...xs), Math.max(...ys)]];
}
