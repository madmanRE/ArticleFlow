from dataclasses import dataclass
from typing import List, Optional


@dataclass
class URLData:
    url: str
    title: Optional[str] = None
    h1: Optional[str] = None
    text: Optional[str] = None
    subheadings: Optional[List[str]] = None
    word_count: Optional[int] = None
    char_count: Optional[int] = None
    subheading_count: Optional[int] = None
    lists_count: Optional[int] = None
    tables_count: Optional[int] = None
