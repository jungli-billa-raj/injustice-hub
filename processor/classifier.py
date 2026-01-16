"""
Crime classifier stub (no LLM yet).
"""

from llm.ollama import OllamaClient
from llm.exceptions import InvalidLLMResponse

classifer_llm = OllamaClient(
    host="192.168.29.210:11434",
    model="smollm2:135m",
)


def classify(headline: str) -> tuple[bool, float]:
    """
    Returns:
    - is_crime (bool)
    - confidence_score (0.0–1.0)
    """

    if not headline:
        return False, 0.0
    #
    # keywords = [
    #     "murder",
    #     "killed",
    #     "rape",
    #     "assault",
    #     "arrest",
    #     "custody",
    #     "police",
    #     "crime",
    #     "firing",
    #     "attack",
    # ]
    #
    # headline_lower = headline.lower()
    # matches = [k for k in keywords if k in headline_lower]
    #
    # if not matches:
    #     return False, 0.2
    #
    # # crude confidence heuristic
    # confidence = min(0.3 + 0.15 * len(matches), 0.9)
    # return True, confidence

    try:
        result = classifer_llm.classify_case(headline)
        print("from classify.py using smollm2")
        print(result)
    except InvalidLLMResponse:
        return False, 0.0

    is_crime = bool(result.get("is_crime", False))
    confidence = float(result.get("confidence", 0.0))

    return is_crime, confidence
