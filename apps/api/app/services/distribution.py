from math import log


def distribution(evidence, field, states):
    votes = [row for row in evidence if row[field] in states and row["weight"] > 0]
    counts = {state: 0.25 for state in states}
    for vote in votes:
        counts[vote[field]] += vote["weight"]
    total = sum(counts.values())
    probabilities = {state: count / total for state, count in counts.items()}
    fresh = [row for row in votes if not row["stale"]]
    flags = []
    if not votes:
        flags.append("UNKNOWN")
    elif not fresh:
        flags.append("STALE")
    if len({row[field] for row in fresh}) > 1:
        flags.append("CONFLICTING")
    if max(probabilities.values()) < 0.75:
        flags.append("UNCERTAIN")
    return {
        "probabilities": probabilities,
        "flags": flags,
        "entropy": -sum(p * log(p) for p in probabilities.values()) / log(len(states)),
    }
