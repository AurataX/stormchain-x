"use client";
import { useState } from "react";
import { post } from "@/lib/api";
import type { Plan } from "@/lib/plan-types";

type Brief = {
  answer: string; citation_ids: string[]; sources: Record<string, string>;
  plan_version: number; model: string; synthetic: boolean;
};

export function Briefing({ plan, assetId }: { plan: Plan; assetId: string | null }) {
  const [question, setQuestion] = useState("Why did the plan change?");
  const [brief, setBrief] = useState<Brief | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function ask() {
    setBusy(true);
    setError(null);
    setBrief(null);
    try {
      setBrief(await post<Brief>("/api/v1/briefings", {
        plan_id: plan.id, question, ...(assetId && { asset_id: assetId }),
      }));
    } catch (cause) {
      setError((cause as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="stack" aria-label="AI briefing">
      <h3>Ask about this plan</h3>
      <p className="muted">Gemini explains saved synthetic evidence. The plan comes from the recovery solver.</p>
      <label htmlFor="brief-question">Question</label>
      <input id="brief-question" value={question} maxLength={400}
        onChange={(event) => setQuestion(event.target.value)} />
      <button onClick={ask} disabled={busy || question.trim().length < 3}>
        {busy ? "Preparing briefing…" : "Ask Gemini"}
      </button>
      {error && <p role="alert" className="tone-failed">{error}</p>}
      {brief && (
        <div role="status" className="stack">
          <p>{brief.answer}</p>
          <p className="muted">AI generated · {brief.model} · plan v{brief.plan_version} · synthetic data</p>
          <details>
            <summary>Saved facts cited ({brief.citation_ids.length})</summary>
            <ul>{brief.citation_ids.map((id) => (
              <li key={id}><strong>{id}</strong><pre>{brief.sources[id]}</pre></li>
            ))}</ul>
          </details>
        </div>
      )}
    </section>
  );
}
