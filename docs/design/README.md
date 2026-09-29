# Operations console design

Direction: a calm, precise coastal operations workspace. The map and recovery
reasoning carry the visual identity. Avoid a generic dashboard grid or
marketing landing page.

Desktop: a slim identity/status bar; 280px scenario rail; flexible map;
360px recovery panel. An asset inspector opens from map selection. Comparison
occupies a focused lower panel only when requested.

Tablet: one collapsible side panel. Mobile: Map, Plan, and Evidence tabs with
one focused panel per view. Preserve selection across views.

Primary action changes with context: Generate plan, then Recalculate after
evidence changes. Include an explicit stale-plan label until a new run completes.

Use concrete language: “Last report: 38 min ago,” “Road access blocked,” and
“Waiting for inspection.” Tooltips explain confidence and simulated data.

Design artifacts:

- [Tokens](tokens.md): palette, spacing, typography, icon rules.
- [Interactions](interactions.md): connected workflows and accessibility.
- [Libraries](libraries.md): verified library sources and selection policy.

Phase 1 establishes this specification only. UI implementation and visual
verification belong to Phase 4; no screenshot or premium-quality claim yet.
The user's map example confirms interest in geographic layers, colored asset
markers, road/dependency lines, a legend, and inspection on selection. It is
interaction inspiration, not a request to copy the supplied screenshot.
