export function toPayload(form: FormData, scenario: string, asset: string) {
  return {
    id: crypto.randomUUID(),
    scenario_id: scenario,
    asset_id: asset,
    source_id: form.get("source"),
    observed_state: form.get("state"),
    access_status: String(form.get("access") ?? "") || null,
    raw_confidence: Number(form.get("confidence")),
    recorded_at: new Date(String(form.get("time"))).toISOString(),
    notes: form.get("notes"),
  };
}
