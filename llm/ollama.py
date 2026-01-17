import requests
import json

from llm.base import LLMClient
from llm.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, CLASSIFIER_PROMPT
from llm.exceptions import InvalidLLMResponse


class OllamaClient(LLMClient):
    """
    LLM Client backed by remote Ollama Server
    """

    def __init__(self, host: str, model: str):
        self.url = f"http://{host}/api/generate"
        self.model = model

    def extract_case(self, article_text: str) -> dict:
        prompt = SYSTEM_PROMPT + USER_PROMPT_TEMPLATE.format(article_text=article_text)
        # print(f"PROMPT:{prompt}\n")

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
            print("Here's the resp.json():")
            data = resp.json()
            print(data)
            raw = data.get("response")
            print("raw")
            print(raw)
            return json.loads(raw)
        except Exception as e:
            # raise InvalidLLMResponse(f"Ollama request failed: {e}")
            print("exception occured from Ollama. Skipping this article:")
            print(type(raw))  # This is coming as NoneType
            if raw is not None:
                print(f"raw response: {raw}")
            print(f"exception: {e}")
            pass

    def classify_case(self, headline: str) -> dict:
        prompt = CLASSIFIER_PROMPT.format(headline=headline)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        try:
            resp = requests.post(self.url, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return json.loads(data["response"])
        except Exception as e:
            raise InvalidLLMResponse(f"Error in classifying case: {e}")
