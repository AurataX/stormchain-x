## 🚨 Selected Hackathon Idea: STORMCHAIN-X

**Track:** Cyclone Impact & Infrastructure Vulnerability Forecaster

**Project:** Cyclone-Aware Infrastructure Intelligence and Resilient Recovery System

### 💡 Concept

STORMCHAIN-X is a software-based decision-support platform that helps determine which infrastructure should be restored or protected first after a cyclone, even when infrastructure data is incomplete, communication networks are disrupted, and asset conditions are uncertain.

Instead of building another cyclone dashboard, we model the relationships between critical infrastructure such as power substations, hospitals, roads, water facilities, shelters, and telecom towers.

### 🔑 Core Features

* **Ground Truth During the Blackout:** Combine incomplete, delayed, conflicting, or simulated observations with source reliability and confidence.
* **Infrastructure Dependency Graph:** Model how failures in one asset can affect hospitals, water systems, roads, and other services.
* **Uncertainty-Aware Scenario Engine:** Simulate different possible infrastructure states and cascading disruptions.
* **Recovery Optimization:** Recommend recovery actions under limited budget, repair teams, road accessibility, and other constraints.
* **Interactive Decision Dashboard:** Show infrastructure impact, uncertainty, recovery priorities, and how recommendations change when new information arrives.

### 🛠️ Technology Stack

* Frontend: Next.js, TypeScript, Tailwind CSS, MapLibre
* Backend: Python, FastAPI
* Simulation: NetworkX, GeoPandas, NumPy, Monte Carlo
* Optimization: OR-Tools / custom optimization heuristics
* Database: PostgreSQL + PostGIS
* Cloud: Google Cloud Run, Cloud SQL, Cloud Storage, Cloud Run Jobs
* Optional AI: Vertex AI/Gemini for explanations and natural-language scenario queries

### ☁️ GCP Usage

* **Cloud Run:** Deploy frontend and backend
* **Cloud SQL:** Store infrastructure assets, dependencies, observations, and scenarios
* **Cloud Storage:** Store datasets, reports, and generated results
* **Cloud Run Jobs:** Execute computationally intensive simulations
* **Secret Manager:** Secure credentials and API secrets
* **Cloud Build + Artifact Registry:** Build and deploy containers

### 🎯 Main Differentiator

The system does not simply predict damage or display cyclone information. It evaluates **how uncertain and incomplete information affects infrastructure recovery decisions**, and updates recovery plans as new evidence becomes available.

Our initial implementation will be software-first using open or synthetic data. Physical sensor nodes and offline communication prototypes can be added later as optional extensions.
