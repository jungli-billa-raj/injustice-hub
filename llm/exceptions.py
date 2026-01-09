class LLMError(Exception):
    """Base class for all LLM-related errors."""

    pass


class InvalidLLMResponse(LLMError):
    """
    Raised when the LLM response:
    - Is not valid JSON
    - Violates the schema
    - Contains invalid enum values
    """

    pass
