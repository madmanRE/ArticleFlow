from typing import List, Optional

from .html_extractor import HtmlExtractor
from .html_tags_parser import HtmlTagsParser
from .url_data import URLData


class HTMLParser:
    def __init__(self, user_agent: str, exclude_tags: Optional[List[str]]) -> None:
        self._extractor = HtmlExtractor(user_agent=user_agent)
        self._tags_parser = HtmlTagsParser(
            subheading_tags=["h2", "h3", "h4", "h5", "h6"],
            list_tags=["ul", "ol"],
            exclude_tags=exclude_tags,
        )

    def parse_docs(self, urls: List[str]) -> List[URLData]:
        result: List[URLData] = []
        for url in urls:
            try:
                content = self._extractor.extract_html(url)
                if not content:
                    continue
                data = self._tags_parser.parse_html(url, content)
                result.append(data)
            except Exception:
                pass
        return result
