from llm.exceptions import InvalidLLMResponse

# raw_output = llm.extract_case(article_text)
# validated = validate_case_json(raw_output)
# now safe to insert into DB


# Allowed enum values (single source of truth)
ENTITY_TYPES = {"individual", "organization"}
BLAME_STATUS = {"accused", "guilty", "liable"}
JUSTICE_STATUS = {"served", "pending", "escaped"}


def validate_case_json(data: dict) -> dict:
    """
    Validates LLM output against the agreed JSON contract
    and database constraints.

    This function:
    - Does NOT modify data
    - Does NOT retry
    - Raises error on first violation

    Returns:
        dict: validated data (unchanged)

    Raises:
        InvalidLLMResponse
    """

    required_fields = {
        "blamed_entity",
        "entity_type",
        "location",
        "crime_description",
        "severity",
        "blame_status",
        "justice_status",
        "confidence_score",
    }

    # 1️⃣ Must be a dict
    if not isinstance(data, dict):
        raise InvalidLLMResponse("LLM output is not a JSON object")

    # 2️⃣ Required fields must exist
    missing = required_fields - data.keys()
    if missing:
        raise InvalidLLMResponse(f"Missing fields: {missing}")

    # 3️⃣ Enum validations
    if data["entity_type"] not in ENTITY_TYPES:
        raise InvalidLLMResponse("Invalid entity_type")

    if data["blame_status"] not in BLAME_STATUS:
        raise InvalidLLMResponse("Invalid blame_status")

    if data["justice_status"] not in JUSTICE_STATUS:
        raise InvalidLLMResponse("Invalid justice_status")

    # 4️⃣ Severity range
    if not isinstance(data["severity"], int) or not (1 <= data["severity"] <= 10):
        raise InvalidLLMResponse("Severity must be integer between 1 and 10")

    # 5️⃣ Confidence range
    if not isinstance(data["confidence_score"], (int, float)) or not (
        0.0 <= data["confidence_score"] <= 1.0
    ):
        raise InvalidLLMResponse("confidence_score must be between 0.0 and 1.0")

    # 6️⃣ Optional field check
    if data["location"] is not None and not isinstance(data["location"], str):
        raise InvalidLLMResponse("location must be string or null")

    return data
