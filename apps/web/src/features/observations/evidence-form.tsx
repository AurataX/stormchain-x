"use client";
import { useState } from "react";
import { post } from "@/lib/api";
import type { Asset, Source } from "@/lib/types";
import { toPayload } from "./payload";

type Props = { asset: Asset | null; scenario: string; sources: Source[]; onSaved: () => void };
const STATES = ["OPERATIONAL", "PARTIALLY_OPERATIONAL", "DAMAGED", "FAILED", "UNKNOWN"];

export function EvidenceForm({ asset, scenario, sources, onSaved }: Props) {
  const [status, setStatus] = useState<{ kind: "idle" | "busy" | "ok" | "error"; text?: string }>({ kind: "idle" });
  if (!asset) return <p className="card">Select an asset to report evidence.</p>;

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus({ kind: "busy" });
    try {
      const body = toPayload(new FormData(event.currentTarget), scenario, asset!.id);
      const saved = await post<{ received_at: string }>("/api/v1/observations", body);
      setStatus({ kind: "ok", text: `Saved at ${new Date(saved.received_at).toLocaleTimeString()}; plan is stale.` });
      onSaved();
    } catch (error) {
      setStatus({ kind: "error", text: (error as Error).message });
    }
  }

  const now = new Date(Date.now() - 60000 - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  return (
    <form key={asset.id} onSubmit={submit} className="card form" aria-label="Report evidence">
      <h2>Report evidence: {asset.name}</h2>
      <label>Source<select name="source">{sources.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}</select></label>
      <label>Observed state<select name="state">{STATES.map((s) => <option key={s}>{s}</option>)}</select></label>
      {asset.type_id === "road" && (
        <label>Road access<select name="access"><option value="">Not reported</option><option>OPEN</option><option>BLOCKED</option><option>UNKNOWN</option></select></label>
      )}
      <label>Confidence (0–1)<input name="confidence" type="number" min="0" max="1" step="0.05" defaultValue="0.8" required /></label>
      <label>Event time<input name="time" type="datetime-local" defaultValue={now} required /></label>
      <label>Notes<input name="notes" maxLength={1000} /></label>
      <button className="primary" disabled={status.kind === "busy"}>
        {status.kind === "error" ? "Retry" : status.kind === "busy" ? "Saving…" : "Submit report"}
      </button>
      {status.text && <p role="status" className={status.kind === "error" ? "tone-failed" : "tone-operational"}>{status.text}</p>}
    </form>
  );
}
