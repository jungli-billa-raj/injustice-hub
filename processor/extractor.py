"""
Structured case extractor stub.
"""


def extract_case(article: dict) -> dict:
    """
    Produces a schema-valid case object.
    """

    return {
        "blamed_entity": "UNKNOWN",
        "entity_type": "individual",  # or "Organization"
        "location": None,
        "crime_description": article["headline"][:300],
        "severity": 5,
        "blame_status": "accused",
        "justice_status": "pending",
    }
