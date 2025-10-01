from collections import defaultdict
from typing import Dict, List


class UrlRanker:
    def __init__(self, max_pos: int = 10):
        self.max_pos = max_pos

    def rank(self, urls_list: List[List[str]]) -> List[str]:
        total_urls: Dict[str, List[int]] = defaultdict(list)
        for urls in urls_list:
            for i, u in enumerate(urls, start=1):
                weight = self.max_pos + 1 - i
                total_urls[u].append(weight)
        ranked = sorted(total_urls.items(), key=lambda x: sum(x[1]), reverse=True)
        return [u for u, _ in ranked[:10]]
