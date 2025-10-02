from typing import Dict, List

from core.document_parser import URLData

from .numeric_stats_extractor import NumericStatsExtractor
from .text_stats_extractor import TextStatExtractor
from .validator import UrlDataValidator



class StatMaker:
    def __init__(self):
        self._text_stat_maker = TextStatExtractor()
        self._numeric_stat_maker = NumericStatsExtractor()
        self._validator = UrlDataValidator()

    def get_stats(self, docs: List[URLData]) -> Dict:
        valid_docs = self._validator.validate_urls(docs)
        if not valid_docs:
            return {"numeric_stats": {}, "text_stats": {}}

        numeric_stats = self._numeric_stat_maker.get_numeric_stats(valid_docs)
        text_stats = self._text_stat_maker.get_text_stats(valid_docs)
        return {"numeric_stats": numeric_stats, "text_stats": text_stats}
