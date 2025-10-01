from typing import List, Set
from urllib.parse import urlparse


class UrlNormalizer:
    def __init__(self, exclude_domains: List[str]):
        self.exclude_domains: Set[str] = {self._get_domain(d) for d in exclude_domains}

    @staticmethod
    def _get_domain(u: str) -> str:
        hostname = urlparse(u).hostname or ''
        parts = hostname.split('.')
        return '.'.join(parts[-2:]) if len(parts) >= 2 else hostname

    def check(self, u: str) -> bool:
        return self._get_domain(u) not in self.exclude_domains

    @staticmethod
    def normalize(u: str) -> str:
        p = urlparse(u)
        return f"{p.scheme}://{p.netloc}{p.path}".rstrip("/")
