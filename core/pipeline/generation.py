from typing import List, Optional

from config import (
    OPENAI_API_KEY,
    OPENROUTER_API_URL,
    XMLRIVER_USER_ID,
    XMLRIVER_USER_KEY,
)
from core.document_parser import HTMLParser
from core.llm import EasyLLM, HardLLM, TextLLM
from core.serp_parser import XmlRiverService
from core.stats import StatMaker


class TextGenerator:
    def __init__(
            self,
            model: str,
            temperature: float = 0.5
    ) -> None:
        self._text_llm = TextLLM(
            base_url=OPENROUTER_API_URL,
            api_key=OPENAI_API_KEY,
            model=model,
            temperature=temperature
        )

    def generate(self, task_description: str) -> str:
        text = self._text_llm.make_response(task_description)
        return text


class TaskGenerator:
    def __init__(
            self,
            queries: Optional[List[str]],
            competitors: Optional[List[str]],
            exclude_domains: Optional[List[str]],
            search_engine: Optional[str],
            device: Optional[str],
            lr: Optional[int],
            loc: Optional[int],
            user_agent: Optional[str],
            exclude_tags: Optional[List[str]],
            model: str,
            doc_type: str,
            additional_prompt: Optional[str],
            temperature: float = 0.5,
            mode: str = "easy"
    ) -> None:
        self._mode = mode
        if mode == "hard":
            self._queries = queries
            self._competitors = competitors
            self._serp_parser = XmlRiverService(
                user_id=XMLRIVER_USER_ID,
                key=XMLRIVER_USER_KEY,
                exclude_domains=exclude_domains,
                search_engine=search_engine,
                device=device,
                lr=lr,
                loc=loc
            )
            self._html_parser = HTMLParser(
                user_agent=user_agent,
                exclude_tags=exclude_tags
            )
            self._stats_maker = StatMaker()
            self._hard_llm = HardLLM(
                base_url=OPENROUTER_API_URL,
                api_key=OPENAI_API_KEY,
                model=model,
                doc_type=doc_type,
                additional_prompt=additional_prompt if additional_prompt else "",
                temperature=temperature
            )
        else:
            self._easy_llm = EasyLLM(
                base_url=OPENROUTER_API_URL,
                api_key=OPENAI_API_KEY,
                model=model,
                additional_prompt=additional_prompt,
                temperature=temperature
            )

    def generate(self) -> str:
        if self._mode == "hard":
            top_urls = self._competitors if self._competitors \
                else self._serp_parser.search(self._queries)
            parsed_documents = self._html_parser.parse_docs(top_urls)
            stats = self._stats_maker.get_stats(parsed_documents)
            technical_task = self._hard_llm.make_response(
                queries=self._queries,
                competitors=self._competitors,
                words=stats.get("words"),
                numeric=stats.get("numeric"),
            )

            return top_urls, technical_task

        else:
            technical_task = self._easy_llm.make_response()
            return None, technical_task
