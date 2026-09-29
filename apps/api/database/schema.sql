-- Generated from SQLAlchemy metadata. Run python scripts/schema.py --write.

CREATE TABLE asset_types (
	id VARCHAR(32) NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	category VARCHAR(32) NOT NULL, 
	criticality_weight DOUBLE PRECISION NOT NULL, 
	CONSTRAINT pk_asset_types PRIMARY KEY (id), 
	CONSTRAINT ck_asset_types_weight CHECK (criticality_weight >= 0)
);

CREATE TABLE observation_sources (
	id VARCHAR(32) NOT NULL, 
	name VARCHAR(64) NOT NULL, 
	base_reliability DOUBLE PRECISION NOT NULL, 
	half_life_seconds INTEGER NOT NULL, 
	CONSTRAINT pk_observation_sources PRIMARY KEY (id), 
	CONSTRAINT ck_observation_sources_reliability CHECK (base_reliability > 0 AND base_reliability <= 1), 
	CONSTRAINT ck_observation_sources_half_life CHECK (half_life_seconds > 0)
);

CREATE TABLE scenarios (
	id VARCHAR(64) NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	description VARCHAR(1000) NOT NULL, 
	cyclone_category INTEGER NOT NULL, 
	communication_mode VARCHAR(32) NOT NULL, 
	budget_cents INTEGER NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	available_crews JSON NOT NULL, 
	CONSTRAINT pk_scenarios PRIMARY KEY (id), 
	CONSTRAINT ck_scenarios_budget CHECK (budget_cents >= 0), 
	CONSTRAINT ck_scenarios_category CHECK (cyclone_category BETWEEN 1 AND 5), 
	CONSTRAINT ck_scenarios_communication CHECK (communication_mode IN ('NORMAL','DEGRADED','SEVERELY_DEGRADED','OFFLINE'))
);

CREATE TABLE assets (
	id VARCHAR(64) NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	type_id VARCHAR(32) NOT NULL, 
	geometry JSON NOT NULL, 
	capacity_metrics JSON NOT NULL, 
	backup_systems JSON NOT NULL, 
	provenance VARCHAR(32) NOT NULL, 
	CONSTRAINT pk_assets PRIMARY KEY (id), 
	CONSTRAINT fk_assets_type_id_asset_types FOREIGN KEY(type_id) REFERENCES asset_types (id)
);

CREATE INDEX ix_assets_type_id ON assets (type_id);

CREATE TABLE recovery_plans (
	id VARCHAR(36) NOT NULL, 
	scenario_id VARCHAR(64) NOT NULL, 
	version INTEGER NOT NULL, 
	total_cost_cents INTEGER NOT NULL, 
	duration_minutes INTEGER NOT NULL, 
	plan_payload JSON NOT NULL, 
	deterministic_rationale JSON NOT NULL, 
	generated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	CONSTRAINT pk_recovery_plans PRIMARY KEY (id), 
	CONSTRAINT uq_recovery_plans_scenario_id UNIQUE (scenario_id, version), 
	CONSTRAINT ck_recovery_plans_cost CHECK (total_cost_cents >= 0), 
	CONSTRAINT ck_recovery_plans_duration CHECK (duration_minutes >= 0), 
	CONSTRAINT ck_recovery_plans_version CHECK (version > 0), 
	CONSTRAINT fk_recovery_plans_scenario_id_scenarios FOREIGN KEY(scenario_id) REFERENCES scenarios (id)
);

CREATE TABLE simulation_runs (
	id VARCHAR(36) NOT NULL, 
	scenario_id VARCHAR(64) NOT NULL, 
	fingerprint VARCHAR(64) NOT NULL, 
	engine_version VARCHAR(32) NOT NULL, 
	inputs JSON NOT NULL, 
	result JSON NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	CONSTRAINT pk_simulation_runs PRIMARY KEY (id), 
	CONSTRAINT fk_simulation_runs_scenario_id_scenarios FOREIGN KEY(scenario_id) REFERENCES scenarios (id)
);

CREATE INDEX ix_simulation_runs_fingerprint ON simulation_runs (fingerprint);

CREATE INDEX ix_simulation_runs_scenario_id ON simulation_runs (scenario_id);

CREATE TABLE dependencies (
	id VARCHAR(64) NOT NULL, 
	source_asset_id VARCHAR(64) NOT NULL, 
	target_asset_id VARCHAR(64) NOT NULL, 
	dependency_type VARCHAR(32) NOT NULL, 
	properties JSON NOT NULL, 
	CONSTRAINT pk_dependencies PRIMARY KEY (id), 
	CONSTRAINT uq_dependencies_source_asset_id UNIQUE (source_asset_id, target_asset_id, dependency_type), 
	CONSTRAINT ck_dependencies_no_self_edge CHECK (source_asset_id <> target_asset_id), 
	CONSTRAINT ck_dependencies_type CHECK (dependency_type IN ('POWER','WATER','TELECOM','ROAD_ACCESS')), 
	CONSTRAINT fk_dependencies_source_asset_id_assets FOREIGN KEY(source_asset_id) REFERENCES assets (id), 
	CONSTRAINT fk_dependencies_target_asset_id_assets FOREIGN KEY(target_asset_id) REFERENCES assets (id)
);

CREATE INDEX ix_dependencies_source_asset_id ON dependencies (source_asset_id);

CREATE INDEX ix_dependencies_target_asset_id ON dependencies (target_asset_id);

CREATE TABLE observations (
	id VARCHAR(36) NOT NULL, 
	scenario_id VARCHAR(64) NOT NULL, 
	asset_id VARCHAR(64) NOT NULL, 
	source_id VARCHAR(32) NOT NULL, 
	observed_state VARCHAR(32) NOT NULL, 
	access_status VARCHAR(16), 
	raw_confidence DOUBLE PRECISION NOT NULL, 
	recorded_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	received_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	notes VARCHAR(1000) NOT NULL, 
	CONSTRAINT pk_observations PRIMARY KEY (id), 
	CONSTRAINT ck_observations_confidence CHECK (raw_confidence BETWEEN 0 AND 1), 
	CONSTRAINT ck_observations_access CHECK (access_status IN ('OPEN','BLOCKED','UNKNOWN')), 
	CONSTRAINT ck_observations_state CHECK (observed_state IN ('OPERATIONAL','PARTIALLY_OPERATIONAL','DAMAGED','FAILED','UNKNOWN')), 
	CONSTRAINT ck_observations_time_order CHECK (recorded_at <= received_at), 
	CONSTRAINT fk_observations_scenario_id_scenarios FOREIGN KEY(scenario_id) REFERENCES scenarios (id), 
	CONSTRAINT fk_observations_asset_id_assets FOREIGN KEY(asset_id) REFERENCES assets (id), 
	CONSTRAINT fk_observations_source_id_observation_sources FOREIGN KEY(source_id) REFERENCES observation_sources (id)
);

CREATE INDEX ix_observations_scenario_asset_time ON observations (scenario_id, asset_id, recorded_at);

CREATE EXTENSION IF NOT EXISTS postgis;

ALTER TABLE assets ADD COLUMN IF NOT EXISTS geom geometry(Geometry, 4326)
GENERATED ALWAYS AS (ST_SetSRID(ST_GeomFromGeoJSON(geometry::text), 4326)) STORED;

CREATE INDEX IF NOT EXISTS ix_assets_geom ON assets USING GIST (geom);
