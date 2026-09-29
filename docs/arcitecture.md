You are a senior systems architect, disaster-resilience researcher, geospatial engineer, optimization engineer, and full-stack engineer.

We are building a hackathon project called:

STORMCHAIN-X
Cyclone-Aware Infrastructure Intelligence and Resilient Recovery System

TRACK:
Cyclone Impact & Infrastructure Vulnerability Forecaster

IMPORTANT:
This is a software-first hackathon project. We have access to Google Cloud Platform and can deploy cloud infrastructure. Physical sensor nodes are optional extensions, NOT a requirement for the MVP.

============================================================
1. CORE PROBLEM
============================================================

Cyclones can disrupt interconnected infrastructure such as:

- Electricity substations
- Hospitals
- Roads
- Water treatment facilities
- Telecom towers
- Emergency shelters
- Fuel/utility facilities
- Other critical infrastructure

The problem is not simply predicting whether an individual infrastructure asset will fail.

The harder problem is:

After a cyclone, infrastructure information may be incomplete, delayed, conflicting, or unavailable because communication networks and observation systems may be disrupted.

Emergency decision-makers therefore need to determine:

1. What infrastructure may be affected?
2. What infrastructure is currently known to be operational, damaged, or unknown?
3. How confident are we in that information?
4. How can failure of one asset propagate through infrastructure dependencies?
5. Which recovery action should be performed first?
6. How does the optimal recovery plan change when new evidence arrives?
7. How should limited budget, repair teams, accessibility, and time constrain recovery?
8. When is it more valuable to gather information about an uncertain asset instead of immediately repairing another asset?

The system should therefore be a:

UNCERTAINTY-AWARE INFRASTRUCTURE RECOVERY DECISION SYSTEM.

It is NOT merely:

- a cyclone dashboard
- a damage classifier
- a chatbot
- a map with markers
- a generic infrastructure risk score
- an LLM wrapper

============================================================
2. CORE SYSTEM STATEMENT
============================================================

Use this as the central definition:

"STORMCHAIN-X is an uncertainty-aware cyclone infrastructure recovery decision system that fuses incomplete and delayed observations, models infrastructure dependencies and cascading disruptions, and generates budget-constrained recovery plans that adapt as new ground truth becomes available."

The system should explicitly distinguish:

KNOWN
UNKNOWN
UNCERTAIN
CONFLICTING
STALE

information.

Do not assume that "no data" means "failed."

============================================================
3. CORE CONCEPT FROM "GROUND TRUTH DURING THE BLACKOUT"
============================================================

Integrate the following concept into STORMCHAIN-X:

GROUND TRUTH DURING THE BLACKOUT

During and after a cyclone, communication and observation channels may be degraded.

The system should therefore support observations arriving through different sources, such as:

- field reports
- sensor observations
- public datasets
- simulated observations
- delayed observations
- satellite-derived observations where available
- infrastructure databases
- emergency operator reports

For the hackathon MVP, observations can be simulated or generated from open datasets.

DO NOT claim that satellite imagery is always unavailable for a fixed 24-72 hour period.

DO NOT claim that private telecom or SCADA feeds are publicly accessible.

DO NOT make unsupported real-world claims.

Instead, model communication and observation degradation as configurable scenarios.

============================================================
4. FIVE CORE SYSTEM LAYERS
============================================================

Design the system around these layers:

LAYER 1 — MULTI-SOURCE GROUND TRUTH

Stores infrastructure observations.

Each observation should contain concepts such as:

- asset_id
- source_type
- timestamp
- observed_state
- confidence/reliability
- geographic information if applicable
- evidence metadata
- freshness
- communication status

Example:

Hospital A:
state = operational
confidence = 0.88
source = field_report
timestamp = recent

Substation B:
state = unknown
confidence = 0.25
source = missing_telemetry

Road C:
state = likely_blocked
confidence = 0.72
source = field_report

The exact probability model must be explicitly documented.

------------------------------------------------------------

LAYER 2 — RESILIENT DATA / COMMUNICATION MODEL

Model:

- delayed observations
- missing observations
- intermittent communication
- conflicting observations
- stale observations
- offline observation buffering
- restored communication

The software should be able to simulate:

NORMAL
DEGRADED
SEVERELY DEGRADED
OFFLINE

communication conditions.

Optional future extension:

ESP32 / Raspberry Pi sensor node that stores observations locally and forwards them when connectivity returns.

Do not make hardware necessary for the core system.

------------------------------------------------------------

LAYER 3 — INFRASTRUCTURE DEPENDENCY GRAPH

Represent infrastructure as a graph.

Nodes may represent:

- hospitals
- substations
- roads
- water plants
- telecom towers
- shelters
- emergency facilities

Edges represent dependencies such as:

POWER_DEPENDENCY
ROAD_ACCESS
TELECOM_DEPENDENCY
WATER_DEPENDENCY
FUNCTIONAL_DEPENDENCY
GEOGRAPHIC_RELATIONSHIP

Example:

Substation A
    |
    +----> Hospital A
    |
    +----> Water Plant B

Road C
    |
    +----> access to Hospital A

If Substation A fails, dependent infrastructure can experience secondary impact.

The dependency model must be explicit and inspectable.

------------------------------------------------------------

LAYER 4 — UNCERTAINTY + CASCADING IMPACT ENGINE

Do NOT use a simplistic:

damage = 0/1

model.

Represent possible asset states such as:

OPERATIONAL
PARTIALLY_OPERATIONAL
DAMAGED
FAILED
UNKNOWN

with confidence/probability where appropriate.

The engine should evaluate multiple possible scenarios.

For example:

Scenario 1:
Substation B operational

Scenario 2:
Substation B partially operational

Scenario 3:
Substation B failed

Then calculate downstream consequences for each scenario.

Use appropriate methods such as:

- Monte Carlo simulation
- Bayesian updating
- probabilistic state transitions
- scenario sampling
- dependency propagation

Choose the simplest method that can be explained and validated within a hackathon.

Do NOT add machine learning merely for appearance.

------------------------------------------------------------

LAYER 5 — RECOVERY DECISION ENGINE

The system should evaluate possible recovery actions.

Examples:

- repair substation
- clear road
- restore telecom
- repair water facility
- verify unknown asset
- deploy temporary power
- restore alternate route
- protect an asset for future hazard

Each action may have:

- cost
- duration
- required team
- required access
- expected service restoration
- dependency effects
- uncertainty
- feasibility constraints

The optimizer must work under constraints such as:

budget
repair teams
road accessibility
time
available resources

Possible approaches:

- OR-Tools
- integer programming
- constraint optimization
- greedy heuristic
- scenario-based optimization

Start simple and transparent.

============================================================
5. IMPORTANT NOVEL DECISION CONCEPT
============================================================

Implement:

INFORMATION VALUE / INFORMATION-GATHERING ACTIONS

Sometimes repairing an asset immediately is not necessarily the best decision because the asset's current condition is unknown.

The system should be able to consider an action like:

"VERIFY SUBSTATION B"

as a legitimate recovery action.

The system can compare:

Repair Substation B now
VS
Verify Substation B first
VS
Repair another asset

The implementation does NOT need to claim formal academic Value of Information unless properly implemented.

A practical hackathon version can calculate:

expected decision improvement
uncertainty reduction
decision sensitivity

and explain the result.

============================================================
6. ADAPTIVE RECOVERY PLANNING
============================================================

This is a core demonstration.

Initial state:

Substation B = unknown
Road C = open
Hospital A = operational

System generates:

RECOVERY PLAN V1

Then introduce new evidence:

Road C = blocked

The system must recalculate the scenario.

Generate:

RECOVERY PLAN V2

Show:

- what changed
- why it changed
- which dependencies were affected
- which actions became infeasible
- which new action became more valuable
- how uncertainty changed

Then introduce another observation:

Substation B = likely failed

Recalculate again.

This demonstrates that STORMCHAIN-X is a dynamic decision system rather than a static dashboard.

============================================================
7. USER EXPERIENCE
============================================================

Build an interactive web application.

Main interface should include:

A. MAP VIEW

Display:

- infrastructure assets
- roads
- hazard area
- dependency relationships
- asset state
- confidence/uncertainty

B. SCENARIO CONTROL PANEL

Allow user to change:

- cyclone intensity
- rainfall/wind impact assumptions
- communication degradation
- asset failure probabilities
- road accessibility
- available budget
- available repair teams
- observation freshness
- infrastructure conditions

C. INFRASTRUCTURE INSPECTOR

When selecting an asset, show:

- current estimated state
- possible states
- confidence
- observations
- source types
- timestamp
- dependencies
- dependent assets
- potential consequences
- available recovery actions

D. RECOVERY PLAN

Show:

- recommended action sequence
- estimated cost
- expected impact reduction
- feasibility
- uncertainty
- affected infrastructure

E. SCENARIO COMPARISON

Compare:

BASELINE
vs
STORMCHAIN-X

and:

PLAN V1
vs
PLAN V2

F. EXPLANATION PANEL

Explain:

"Why did the recovery plan change?"

Use deterministic information generated by the underlying model.

An LLM may optionally convert structured results into natural language, but it must NOT invent scientific facts.

============================================================
8. EVALUATION
============================================================

The project must be measurable.

Create baseline strategies such as:

BASELINE 1:
Highest individual asset criticality first.

BASELINE 2:
Highest estimated damage first.

BASELINE 3:
Nearest repair action first.

BASELINE 4:
Random feasible recovery plan.

Compare them with STORMCHAIN-X.

Possible metrics:

- service restoration
- affected critical infrastructure
- recovery cost
- recovery time
- number of dependent services restored
- uncertainty reduction
- constraint violations
- robustness under missing information

Be careful with metrics.

Do not invent real-world performance claims.

Use simulated or open data and clearly label results.

============================================================
9. EXPERIMENTS
============================================================

Design reproducible experiments.

At minimum:

EXPERIMENT A:
Complete information

EXPERIMENT B:
20% observations missing

EXPERIMENT C:
50% observations missing

EXPERIMENT D:
Delayed observations

EXPERIMENT E:
Conflicting observations

EXPERIMENT F:
Communication outage

EXPERIMENT G:
Limited recovery budget

EXPERIMENT H:
Limited repair teams

EXPERIMENT I:
Road accessibility disruption

EXPERIMENT J:
New evidence arrives during recovery

Show how the decision system responds.

============================================================
10. DATA STRATEGY
============================================================

Do not depend on proprietary infrastructure data.

Use:

- open geospatial datasets
- public infrastructure datasets where available
- OpenStreetMap where appropriate
- publicly available hazard data
- synthetic infrastructure dependencies
- controlled scenario generation

Clearly separate:

REAL DATA
from
SYNTHETIC DATA
from
SIMULATED OBSERVATIONS

If a real dataset cannot be reliably accessed, generate a synthetic dataset with realistic structure and clearly document the assumptions.

Do not fabricate measurements.

============================================================
11. GCP ARCHITECTURE
============================================================

We have access to Google Cloud.

Recommended architecture:

Frontend:
Next.js

Backend:
FastAPI

Database:
Cloud SQL PostgreSQL + PostGIS

Object storage:
Cloud Storage

Application deployment:
Cloud Run

Heavy simulation:
Cloud Run Jobs

Messaging:
Pub/Sub if useful

Secrets:
Secret Manager

Container registry:
Artifact Registry

CI/CD:
Cloud Build

Monitoring:
Cloud Logging / Cloud Monitoring

Optional AI:
Vertex AI / Gemini

Do not use every GCP service merely for demonstration.

Use only services that have a clear architectural purpose.

============================================================
12. OPTIONAL GEMINI / VERTEX AI
============================================================

If adding Gemini, use it for:

- scenario explanation
- natural language queries
- evidence summarization
- structured report generation
- "why did the plan change?" explanations

Do NOT allow the LLM to directly determine:

- infrastructure failure probabilities
- emergency priorities
- physical hazard predictions
- scientific measurements

The deterministic simulation/optimization engine must remain the source of truth.

============================================================
13. SOFTWARE ARCHITECTURE
============================================================

Recommend a practical repository architecture.

Suggested starting point:

stormchain-x/

apps/
  web/
  api/

services/
  graph_engine/
  scenario_engine/
  fusion_engine/
  recovery_engine/

data/
  assets/
  scenarios/
  observations/

experiments/
  baselines/
  evaluation/

infra/
  docker/
  gcp/

docs/

Do NOT over-engineer the project with unnecessary microservices.

A modular FastAPI backend is acceptable for the MVP.

============================================================
14. DATABASE DESIGN
============================================================

Design a normalized schema for at least:

assets
asset_types
dependencies
observations
observation_sources
scenarios
scenario_parameters
asset_states
recovery_actions
recovery_plans
simulation_runs
simulation_results
communication_events

Include:

- primary keys
- foreign keys
- timestamps
- spatial fields where appropriate
- indexes
- PostGIS geometry
- relationships

Explain why each table exists.

============================================================
15. API DESIGN
============================================================

Design REST APIs such as:

GET /assets
GET /assets/{id}
GET /assets/{id}/dependencies

POST /observations
GET /observations

POST /scenarios
GET /scenarios/{id}

POST /simulations/run
GET /simulations/{id}

POST /recovery/optimize
GET /recovery/plans/{id}

POST /communication/events

GET /infrastructure/graph

Design proper Pydantic schemas.

============================================================
16. SECURITY
============================================================

Implement reasonable application security.

Use:

- authentication if required
- authorization
- input validation
- environment variables
- Secret Manager
- rate limiting where appropriate
- audit logs for decision changes
- no hardcoded credentials

Do not build unsafe autonomous emergency-control functionality.

This is a decision-support prototype.

============================================================
17. DEVELOPMENT PLAN
============================================================

Give a realistic hackathon execution plan.

Phase 1:
Architecture + database + sample dataset

Phase 2:
Infrastructure graph

Phase 3:
Observation / ground truth system

Phase 4:
Communication degradation simulation

Phase 5:
Uncertainty engine

Phase 6:
Cascading impact simulation

Phase 7:
Recovery optimization

Phase 8:
Frontend map/dashboard

Phase 9:
Evaluation and baselines

Phase 10:
GCP deployment

Phase 11:
Demo scenario

Phase 12:
Polish + documentation

Prioritize a functioning vertical slice early.

============================================================
18. DEMO SCENARIO
============================================================

Design one compelling end-to-end demonstration.

Example:

A cyclone approaches a coastal/urban region.

Several infrastructure assets are potentially affected.

Communication becomes degraded.

Some asset observations are missing.

The system initially generates Recovery Plan V1.

Then:

Observation 1:
A road is reported blocked.

System updates.

Observation 2:
A substation reports an uncertain status.

System updates.

Observation 3:
A field report arrives confirming partial damage.

System updates.

The recovery optimizer recalculates.

The UI shows:

BEFORE
AFTER

and explains:

WHY THE PLAN CHANGED.

The demo should take approximately 3-5 minutes.

============================================================
19. ENGINEERING QUALITY
============================================================

Produce:

- clean architecture
- type safety
- tests
- deterministic simulations where possible
- reproducible experiments
- logging
- error handling
- API documentation
- README
- Docker setup
- environment configuration
- GCP deployment instructions

Do not generate fake APIs or placeholder functionality while claiming it is complete.

If something is mocked, label it clearly as MOCK/SIMULATED.

============================================================
20. RESEARCH POSITIONING
============================================================

Do NOT claim:

"Nobody has ever solved this."

Do NOT claim:

"This is the first system of its kind."

Do NOT claim:

"Satellite imagery is unavailable for 24-72 hours."

Do NOT claim:

"Telecom outage feeds are publicly available."

Instead explain:

The project integrates several known concepts into a prototype focused on cyclone recovery decision-making under incomplete and disrupted information.

Identify which components are established research areas and which integration/design choices are the project's engineering contribution.

============================================================
21. YOUR TASK
============================================================

Now act as the lead architect.

Before writing implementation code:

1. Critically analyze the concept.
2. Identify technical weaknesses.
3. Identify unnecessary features.
4. Identify the minimum viable architecture.
5. Propose the strongest system architecture.
6. Design the database.
7. Design the core algorithms.
8. Define the uncertainty model.
9. Define the infrastructure graph model.
10. Define the cascading impact algorithm.
11. Define the recovery optimization formulation.
12. Define the information-gathering/verification mechanism.
13. Define the API architecture.
14. Define the frontend architecture.
15. Define the GCP architecture.
16. Define the experiment/evaluation framework.
17. Define the complete hackathon implementation plan.
18. Define the final 3-5 minute demo.
19. Identify what should NOT be built.
20. Then provide the recommended implementation roadmap.

Be technically critical.

Do not simply agree with the project.

If a component is unrealistic, unnecessary, unsupported, or too ambitious for a hackathon, explicitly say so and propose a simpler alternative.

Optimize for:

TECHNICAL DEPTH
RESEARCH CREDIBILITY
IMPLEMENTABILITY
DEMONSTRABILITY
REPRODUCIBILITY
CLEAR DIFFERENTIATION

not for the number of technologies used.

At the end, provide:

A. FINAL ARCHITECTURE
B. FINAL TECH STACK
C. FINAL GCP SERVICES
D. DATABASE SCHEMA
E. CORE ALGORITHMS
F. API DESIGN
G. FRONTEND STRUCTURE
H. EXPERIMENT PLAN
I. DEMO SCRIPT
J. HACKATHON BUILD ORDER
K. RISKS AND MITIGATIONS
L. FEATURES TO CUT
M. FEATURES TO ADD ONLY IF TIME REMAINS