# from llm.base import LLMClient
# from llm.prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, CLASSIFIER_PROMPT
from llm.exceptions import InvalidLLMResponse
import requests

model = "smollm2:135m"

print("Why is Cancer such a dangerous disease?")
# prompt = USER_PROMPT_TEMPLATE + SYSTEM_PROMPT.format(article_text=article_text)

payload = {
    "model": model,
    "prompt": "Why is Cancer such a dangerous disease?",
    "stream": False,
    "format": "json",
}
url = "http://192.168.29.210:11434/api/generate"

try:
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
except requests.RequestException as e:
    raise InvalidLLMResponse(f"Ollama request failed: {e}")
