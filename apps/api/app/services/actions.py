# SYNTHETIC repair catalog: illustrative costs/durations, not engineering estimates.
# Keys are asset type ids; crew types match scenario.available_crews.
CATALOG = {
    "substation": {"crew_type": "electrical", "cost_cents": 9_000_000, "duration_hours": 18},
    "hospital": {"crew_type": "generator", "cost_cents": 4_000_000, "duration_hours": 8},
    "water": {"crew_type": "civil", "cost_cents": 7_000_000, "duration_hours": 16},
    "telecom": {"crew_type": "electrical", "cost_cents": 2_500_000, "duration_hours": 10},
    "road": {"crew_type": "civil", "cost_cents": 3_000_000, "duration_hours": 12},
    "shelter": {"crew_type": "civil", "cost_cents": 5_000_000, "duration_hours": 14},
    "depot": {"crew_type": "civil", "cost_cents": 4_000_000, "duration_hours": 10},
}
