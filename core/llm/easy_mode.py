from typing import Dict, List

from .base import BaseLLM
from .llm_client import LLMClient
from .prompts import easy_system_prompt


class EasyLLM(BaseLLM):
    def __init__(
            self,
            base_url: str,
            api_key: str,
            model: str,
            additional_prompt: str | None = None,
            temperature: float = 0.5,
    ) -> None:
        self._additional_prompt = additional_prompt
        self._llm = LLMClient(
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=temperature
        )

    def make_response(
            self,
    ) -> str:
        messages = self._generate_messages()
        resp = self._llm.make_response(messages)
        return resp

    def _generate_messages(self) -> List[Dict]:
        messages = [
            {"role": "system", "content": easy_system_prompt},
            {"role": "user", "content": self._additional_prompt},
        ]

        return messages
