# Reproducible run storage

`simulation_runs` adds immutable-by-API input/result records. Each stores UUID,
scenario reference, SHA-256 fingerprint, engine version, complete evidence,
infrastructure, source parameters, scenario constraints, run settings, result,
Python/NetworkX runtime versions, and creation time. No update/delete endpoint exists.

The fingerprint hashes sorted canonical JSON containing inputs and engine
version. Two identical requests against identical eligible data reproduce the
result and fingerprint but receive distinct run IDs. Changing evidence after
the cutoff cannot alter a saved run.

Simulation uses a local Python RNG and sorted asset IDs. It does not alter
global random state. Replay requires the recorded engine and dependency/runtime
versions; upgrade behavior must be reviewed, never assumed identical.

Workload limits: 100 assets, 500 edges, 100 sources, 10,000 eligible reports,
1,000 samples, 168-hour horizon. Oversized snapshots return 422. CPU work runs
off the async request loop; this remains a local demo, not a public compute API.

Snapshots include current static asset/type/source definitions. Historical
infrastructure edits are not reconstructed. Those tables have no write API;
if editing them is added, introduce versioned topology/source definitions.

References: [NetworkX graph types](https://networkx.org/documentation/stable/reference/introduction.html)
and [Python RNG reproducibility](https://docs.python.org/3.12/library/random.html#notes-on-reproducibility).
