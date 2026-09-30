# Compact console direction — 2026-09-30

Mood: calm operations workspace with dense, readable evidence and recovery context.
Evidence: existing tokens, the current connected console, and the user's Google Maps sample.
Accent: existing blue (#175CD3 light / #69B7FF dark); semantic colors remain status-only.
Reason: retain the established infrastructure identity and reserve green for operational status.

Acceptance: Google Maps advanced markers select the same assets as the table;
roads and dependencies retain overlays, selected and planned assets retain rings.
Map fits synthetic coastal geometry, never the sample's US center. Loading,
missing key, network failure and authorization failure show actionable messages.
The asset table remains available if Google Maps cannot load.

Density: replace separated KPI cards with one divided summary strip; move fixed
scenario constraints above the map; reduce card gaps/padding to 12px; use a
viewport-relative map height; keep the plan beside the map on desktop and tabs
on smaller screens. Put the legend below the map so Google attribution stays visible.

Google key is configured only in ignored local environment; no cloud APIs,
billing, IAM, or deployment configuration are changed. Google authorization and
billing remain external dependencies. Browser checks must distinguish real
Google rendering from mocked integration tests.
