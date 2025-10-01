from typing import Optional

import requests


class ApiClient:
    def __init__(
            self,
            user_id: int,
            key: str,
            device: str,
            groupby: int = 10,
            lr: int = 213,
            country: int = 2643,
            lang: str = "ru",
            loc: int = 20950
    ) -> None:
        self.user_id = user_id
        self.key = key
        self.device = device
        self.groupby = groupby
        self.lr = lr
        self.country = country
        self.lang = lang
        self.loc = loc

    def fetch(self, query: str, engine: str) -> Optional[str]:
        url = "http://xmlriver.com/search_yandex/xml" if engine == "Yandex" else "http://xmlriver.com/search/xml"
        params = {
            "user": self.user_id,
            "key": self.key,
            "query": query,
            "device": self.device,
            "groupby": self.groupby,
        }
        if engine == "Yandex":
            params.update({"lr": self.lr})
        else:
            params.update({"country": self.country, "lr": self.lang, "loc": self.loc})
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.ok:
                return r.text
        except requests.RequestException:
            return None
        return None
