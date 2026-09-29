# Interaction and visual acceptance

Selecting an asset synchronizes map highlight, inspector, related dependencies,
and any recovery actions. Constraints belong to a scenario; edits mark existing
results stale rather than silently changing their interpretation.

Observation submission validates locally and on the API. Show source and event
time, retain receipt time, confirm persistence, then invalidate evidence/results.
On network failure preserve form values and offer a deliberate retry.

Motion: CSS opacity/transform transitions at 150–250ms. Use Motion only for
inspector/timeline continuity when CSS cannot express it. Reduced-motion mode
removes movement. No continuously pulsing warnings or decorative particles.

Accessibility: visible keyboard focus, semantic buttons, dialog focus return,
44px touch targets, readable contrast, status text alongside colors, and an
asset table alternative to the map. Charts include units and textual summaries.

Browser acceptance at 360/768/1280px: no clipped primary action, no accidental
horizontal page scrolling, usable empty/error states, stable layout during loading.
Test keyboard-only evidence entry and map-to-plan selection.

Map attribution remains visible. If external tiles fail, show local synthetic
geometry and an explicit basemap-unavailable state. Never display “live” for fixtures.
