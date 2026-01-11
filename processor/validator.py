"""
Validates extracted case JSON before DB insert.
"""

from processor.schema import CASE_SCHEMA


def validate_case(case: dict) -> bool:
    """
    Returns True if case is valid, else False.
    Never raises.
    """

    # 1. Required fields
    for field in CASE_SCHEMA["required"]:
        if field not in case or case[field] is None:
            return False

    # 2. Enum checks
    if case["entity_type"] not in CASE_SCHEMA["entity_type"]:
        return False

    if case["blame_status"] not in CASE_SCHEMA["blame_status"]:
        return False

    if case["justice_status"] not in CASE_SCHEMA["justice_status"]:
        return False

    # 3. Severity bounds
    if not isinstance(case["severity"], int):
        return False

    if not (
        CASE_SCHEMA["severity_min"] <= case["severity"] <= CASE_SCHEMA["severity_max"]
    ):
        return False

    # All checks passed
    return True
