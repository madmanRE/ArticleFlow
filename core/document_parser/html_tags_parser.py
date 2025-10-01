from typing import List

from bs4 import BeautifulSoup

from .url_data import URLData


class HtmlTagsParser:
    def __init__(
            self,
            subheading_tags: List[str],
            list_tags: List[str],
            exclude_tags: List[str] | None = None
    ) -> None:
        self._exclude_tags = exclude_tags or []
        self._subheading_tags = subheading_tags
        self._list_tags = list_tags

    def parse_html(self, url: str, content: str) -> URLData:
        soup = BeautifulSoup(content, "html.parser")

        for tag in soup(self._exclude_tags):
            tag.decompose()

        data = URLData(url=url)

        title_tag = soup.find("title")
        data.title = title_tag.get_text(strip=True) if title_tag else None

        h1_tag = soup.find("h1")
        data.h1 = h1_tag.get_text(strip=True) if h1_tag else None

        subheadings = soup.find_all(self._subheading_tags)
        data.subheadings = [
            h.get_text(strip=True) for h in subheadings if h.get_text(strip=True)
        ]
        data.subheading_count = len(data.subheadings)

        lists = soup.find_all(self._list_tags)
        data.lists_count = len(lists)

        tables = soup.find_all("table")
        data.tables_count = len(tables)

        text_content = soup.get_text(separator=" ", strip=True)
        data.text = text_content
        data.word_count = len(text_content.split()) if text_content else 0
        data.char_count = len(text_content)

        return data
