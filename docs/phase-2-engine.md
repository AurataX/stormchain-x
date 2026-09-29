# Evidence and cascade semantics

Only observations received and recorded by the requested UTC cutoff are eligible.
Latest physical and latest explicit access event per asset/source win independently;
receipt time and ID break ties. All eligible
reports remain stored in the snapshot. Cross-source correlation is not modeled.

Physical prior: equal 0.25 counts for OPERATIONAL, PARTIALLY_OPERATIONAL,
DAMAGED, FAILED. UNKNOWN never adds a physical vote. Effective count is
reliability × raw confidence × 2^(-age/source-half-life). Report the normalized
distribution and normalized entropy. No usable physical votes → UNKNOWN;
all votes older than two half-lives → STALE; differing fresh source states →
CONFLICTING; maximum probability below 0.75 → UNCERTAIN.

Access uses a separate OPEN/BLOCKED distribution with prior count 0.25 each.
UNKNOWN or absent access reports do not invent closure; absence does not erase
an earlier explicit access report. The same decay/flag rules apply.
Directed ROAD_ACCESS edges originate from a depot. Uncertain road/depot nodes
are removed for conservative reachability but retained for possible routes.
BLOCKED means no possible modeled route, not a measured flood depth. Monte
Carlo samples passability separately. Failed roads and damaged/failed depots
are unavailable; damaged roads can remain open. No physical road
repair, flood recession, or fuel delivery is modeled.

Sampled capacities are 1, 0.5, 0.25, 0. Same-type supplies are redundant via
maximum; required types combine by minimum. Telecom is informational unless
required_for_service is explicit. Backup covers power by min(1, reserve/horizon).
Monotone propagation starts at zero; unanchored cycles supply nothing.

Loss counts healthcare/shelter criticality weights once per service node.
It is not population affected. Horizon averaging, independent samples, and
threshold dependencies are approximations; no engineering flow conservation.
