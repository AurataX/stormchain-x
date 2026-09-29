from app.schemas.common import Output


class ScenarioOutput(Output):
    id: str
    name: str
    description: str
    cyclone_category: int
    communication_mode: str
    budget_cents: int
    currency: str
    available_crews: dict[str, int]


class SourceOutput(Output):
    id: str
    name: str
    base_reliability: float
    half_life_seconds: int
