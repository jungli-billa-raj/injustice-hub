"""
Crime classifier stub (no LLM yet).
"""


def classify(headline: str) -> tuple[bool, float]:
    """
    Returns:
    - is_crime (bool)
    - confidence_score (0.0–1.0)
    """

    if not headline:
        return False, 0.0

    keywords = [
        "murder",
        "killed",
        "rape",
        "assault",
        "arrest",
        "custody",
        "police",
        "crime",
        "firing",
        "attack",
    ]

    headline_lower = headline.lower()
    matches = [k for k in keywords if k in headline_lower]

    if not matches:
        return False, 0.2

    # crude confidence heuristic
    confidence = min(0.3 + 0.15 * len(matches), 0.9)
    return True, confidence
