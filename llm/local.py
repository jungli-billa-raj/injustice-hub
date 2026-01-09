from llm.base import LLMClient

# Usage:
# llm = LocalLLMClient()
# case = llm.extract_case(article_text)


class LocalLLMClient(LLMClient):
    """
    Temporary local LLM implementation.

    For now, this can:
    - Return hardcoded data
    - Or later call a local HTTP model
    """

    def extract_case(self, article_text: str):
        """
        MVP stub implementation.

        This will be replaced with a real model call.
        """

        # NOTE:
        # We deliberately return a fixed structure
        # so the rest of the system can be built safely.

        return {
            "blamed_entity": "Unknown",
            "entity_type": "individual",
            "location": None,
            "crime_description": "Placeholder description",
            "severity": 5,
            "blame_status": "accused",
            "justice_status": "pending",
            "confidence_score": 0.5,
        }
