# SYNTHETIC repair catalog: illustrative costs/durations, not engineering estimates.
# Keys are asset type ids; crew types match scenario.available_crews.
CATALOG = {
    "substation": {"crew_type": "electrical", "cost_cents": 90_000_000, "duration_hours": 18},
    "hospital": {"crew_type": "generator", "cost_cents": 40_000_000, "duration_hours": 8},
    "water": {"crew_type": "civil", "cost_cents": 70_000_000, "duration_hours": 16},
    "telecom": {"crew_type": "electrical", "cost_cents": 25_000_000, "duration_hours": 10},
    "road": {"crew_type": "civil", "cost_cents": 30_000_000, "duration_hours": 12},
    "shelter": {"crew_type": "civil", "cost_cents": 50_000_000, "duration_hours": 14},
    "depot": {"crew_type": "civil", "cost_cents": 40_000_000, "duration_hours": 10},
}
