"""
Canonical JSON schema for a Case.
This must match the SQLite `cases` table.
"""

CASE_SCHEMA = {
    "required": [
        "blamed_entity",
        "entity_type",
        "crime_description",
        "severity",
        "blame_status",
        "justice_status",
    ],
    "entity_type": {"individual", "organization"},
    "blame_status": {"accused", "guilty", "liable"},
    "justice_status": {"pending", "served", "escaped"},
    "severity_min": 1,
    "severity_max": 10,
}
