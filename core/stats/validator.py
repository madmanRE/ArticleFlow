from typing import List

from core.document_parser import URLData


class UrlDataValidator:
    def validate_urls(self, docs: List[URLData]) -> List[URLData]:
        valid_docs = [
            doc for doc in docs if isinstance(doc, URLData) and doc and doc.text
        ]
        return valid_docs
