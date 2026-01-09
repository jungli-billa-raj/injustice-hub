from abc import ABC, abstractmethod
from typing import Dict


class LLMClient(ABC):
    """
    Abstract base class for ALL LLM backends.

    Any LLM (local, OpenAI, Claude, etc.)
    MUST implement this interface.

    This guarantees:
    - Same input
    - Same output shape
    - Backend can be swapped safely
    """

    @abstractmethod
    def extract_case(self, article_text: str) -> Dict:
        """
        Given raw article text, return a SINGLE JSON-compatible dict
        matching the LLM JSON contract.

        This method MUST:
        - Return a Python dict
        - Match the agreed schema
        - Raise an error if extraction fails

        Parameters:
            article_text (str): Full article text

        Returns:
            Dict: structured injustice data
        """
        pass
