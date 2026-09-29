# Phase 2 implementation contract

Scope: snapshot evidence, explain uncertainty, load typed dependencies, assess
access, simulate cascades, and persist reproducible runs. No optimizer or UI yet.

Evidence: evaluate only observations both recorded and received by `as_of`.
Keep latest per asset/source, so polling cannot inflate certainty. Unknown
reports carry no physical-state vote. Four physical states use prior counts
0.25 each; effective weight = reliability × confidence × 2^(-age/half-life).
Return posterior, evidence IDs, freshness, conflicts, missingness and uncertainty.
These are transparent heuristic distributions, not calibrated failure forecasts.

Graph: NetworkX MultiDiGraph preserves edge types. ROAD_ACCESS is directed.
Explicit OPEN/BLOCKED/UNKNOWN reports model passability independently of physical
damage. Failed road samples remain unusable; damaged roads can stay open.
Missing evidence yields unknown access. Report conservative and possible routes.
Same-type supply is redundant (maximum); required types combine via minimum.
Telecom affects service only if explicitly flagged `required_for_service`.

Cascades: start from zero service and iterate upward to the least fixed point,
bounded by asset count plus two. Intrinsic capacity caps service. Generator or
battery reserve covers power over a specified horizon. No fuel deliveries are
assumed. Unanchored supply cycles cannot create service spontaneously.

Use local seeded RNG, bounded samples/graph size, weighted critical-service
loss (not population), per-asset mean service and route-access probability.
Persist complete inputs, parameters, version, fingerprint and output; expose
authorized POST plus read-only retrieval. Test reproducibility and isolation.
