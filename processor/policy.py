"""
Decision policies for inserting cases.
"""

MIN_CONFIDENCE = 0.6


def should_accept_case(is_crime: bool, confidence: float) -> bool:
    """
    Central place to decide whether a case is accepted.
    """
    if not is_crime:
        return False

    if confidence < MIN_CONFIDENCE:
        return False

    return True
