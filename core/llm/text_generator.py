from .llm_client import LLMClient
from typing import List, Dict


class TextLLM:
    def __init__(
            self,
            base_url: str,
            api_key: str,
            model: str,
            temperature: float = 0.5,
    ) -> None:
        self._llm = LLMClient(
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=temperature
        )

    def make_response(
            self,
            task_description: str,
    ) -> str:
        messages = self._generate_messages(task_description)
        resp = self._llm.make_response(messages)
        return resp

    def _generate_messages(self, task_description: str) -> List[Dict]:
        messages = [
            {"role": "system", "content": "Напиши SEO оптимизированный, бизнес ориентированный текст по ТЗ"},
            {"role": "user", "content": task_description}
        ]
        return messages
