from typing import Optional

import requests


class HtmlExtractor:
    def __init__(self, user_agent: str) -> None:
        self._user_agent = user_agent

    def extract_html(self, url: str) -> Optional[str]:
        try:
            r = requests.get(
                url,
                headers={"User-Agent": self._user_agent, "Accept-Charset": "utf-8"},
                timeout=30,
                allow_redirects=True,
            )
            if r.status_code == 200:
                return r.text
        except requests.RequestException:
            pass
        return None
