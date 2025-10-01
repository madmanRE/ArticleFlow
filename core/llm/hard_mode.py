from typing import Dict, List

from .base import BaseLLM
from .llm_client import LLMClient
from .prompts import hard_system_prompt, hard_user_prompt


class HardLLM(BaseLLM):
    def __init__(
            self,
            base_url: str,
            api_key: str,
            model: str,
            doc_type: str,
            additional_prompt: str | None = None,
            temperature: float = 0.5,
    ) -> None:
        self._doc_type = doc_type
        self._additional_prompt = additional_prompt
        self._llm = LLMClient(
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=temperature
        )

    def make_response(
            self,
            queries: List[str],
            competitors: List[Dict],
            words: Dict,
            numeric: Dict
    ) -> str:
        messages = self._generate_messages(
            doc_type=self._doc_type,
            queries=queries,
            competitors=competitors,
            words=words,
            numeric=numeric
        )
        resp = self._llm.make_response(messages)
        return resp

    def _generate_messages(
            self,
            doc_type: str,
            queries: List[str],
            competitors: List[Dict],
            words: Dict,
            numeric: Dict
    ) -> List[Dict]:
        user_prompt = hard_user_prompt.format(
            doc_type=doc_type,
            queries=queries,
            competitors=competitors,
            words=words,
            numeric=numeric
        )

        if self._additional_prompt:
            user_prompt += f"\n\n{self._additional_prompt}"

        messages = [
            {"role": "system", "content": hard_system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        return messages
