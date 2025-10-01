from typing import List

from .api_client import ApiClient
from .url_normalizer import UrlNormalizer
from .url_ranker import UrlRanker
from .xml_parser import XmlParser


class XmlRiverService:
    def __init__(
            self,
            user_id: int,
            key: str,
            exclude_domains: List[str],
            search_engine: str,
            device: str,
            lr: int,
            loc: int
    ) -> None:
        self.api = ApiClient(user_id=user_id, key=key, device=device, lr=lr, loc=loc)
        self.parser = XmlParser()
        self.normalizer = UrlNormalizer(exclude_domains=exclude_domains)
        self.rank = UrlRanker(max_pos=10)
        self.search_engine = search_engine

    def search(self, queries: List[str]) -> List[str]:
        all_urls = []
        for q in queries:
            xml = self.api.fetch(q, self.search_engine)
            if not xml:
                continue
            urls = self.parser.extract_urls(self.parser.parse(xml))
            urls = [
                self.normalizer.normalize(u) for u in urls if self.normalizer.check(u)
            ]
            all_urls.append(urls)
        return self.rank.rank(all_urls)
