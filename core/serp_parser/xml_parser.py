from typing import Dict, List

import xmltodict


class XmlParser:
    @staticmethod
    def parse(xml: str) -> Dict:
        try:
            return xmltodict.parse(xml)
        except Exception:
            return {}

    @staticmethod
    def extract_urls(data: Dict) -> List[str]:
        urls = []
        try:
            groups = (data.get("yandexsearch", {})
            .get("response", {})
            .get("results", {})
            .get("grouping", {})
            .get("group", []))
            if not isinstance(groups, list):
                groups = [groups]
            for group in groups:
                doc = group.get("doc")
                if isinstance(doc, dict):
                    url = doc.get("url")
                    if url:
                        urls.append(url)
        except Exception:
            pass
        return urls
