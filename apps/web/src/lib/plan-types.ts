export type Action = {
  id: string;
  crew_type: string;
  cost_cents: number;
  duration_hours: number;
  start_hour: number;
  end_hour: number;
};
export type Plan = {
  id: string;
  version: number;
  total_cost_cents: number;
  duration_minutes: number;
  generated_at: string;
  plan_payload: {
    actions: Action[];
    solver: { status: string; objective: number | null; gap: number | null };
    unselected: string[];
    verification_priority: { asset_id: string; score: number; flags: string[] }[];
    assumptions: string[];
  };
  deterministic_rationale: {
    previous_version: number | null;
    diff: { added: string[]; removed: string[]; rescheduled: string[] };
  };
};
