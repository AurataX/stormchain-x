from pydantic import BaseModel


class EvidenceWeight(BaseModel):
    id: str
    state: str
    weight: float
    age_seconds: float
    stale: bool
    access_status: str | None


class Assessment(BaseModel):
    probabilities: dict[str, float]
    flags: list[str]
    evidence: list[EvidenceWeight]
    entropy: float
    passability: dict


class GraphOutput(BaseModel):
    scenario_id: str
    as_of: str
    assets: list[dict]
    dependencies: list[dict]
    assessments: dict[str, Assessment]
    access: dict[str, str]
