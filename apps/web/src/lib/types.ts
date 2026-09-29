export type Report = { probabilities: Record<string, number>; flags: string[]; entropy: number };
export type Assessment = Report & { passability: Report };
export type Asset = {
  id: string;
  name: string;
  type_id: string;
  geometry: { type: string; coordinates: number[] | number[][] };
};
export type Edge = {
  id: string;
  source_asset_id: string;
  target_asset_id: string;
  dependency_type: string;
};
export type Graph = {
  as_of: string;
  assets: Asset[];
  dependencies: Edge[];
  assessments: Record<string, Assessment>;
  access: Record<string, string>;
};
export type Scenario = {
  id: string;
  name: string;
  description: string;
  budget_cents: number;
  currency: string;
  communication_mode: string;
  available_crews: Record<string, number>;
};
export type Source = { id: string; name: string };
export type Observation = {
  id: string;
  source_id: string;
  observed_state: string;
  access_status: string | null;
  recorded_at: string;
  notes: string;
};
export type AssetDetail = { asset: Asset; observations: Observation[]; dependencies: Edge[] };
