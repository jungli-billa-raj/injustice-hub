import requests
import json

from llm.base import LLMClient
from llm.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from llm.exceptions import InvalidLLMResponse


class OllamaClient(LLMClient):
    """
    LLM Client backed by remote Ollama Server
    """

    def __init__(self, host: str, model: str):
        self.url = f"http://{host}/api/generate"
        self.model = model

    def extract_case(self, article_text: str) -> dict:
        prompt = USER_PROMPT_TEMPLATE + SYSTEM_PROMPT.format(article_text=article_text)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        try:
            resp = requests.post(self.url, json=payload, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise InvalidLLMResponse(f"Ollama request failed: {e}")

        try:
            data = resp.json()
            raw = data.get("resposne")
            return json.loads(raw)
        except Exception as e:
            raise InvalidLLMResponse(f"Ollama request failed: {e}")
