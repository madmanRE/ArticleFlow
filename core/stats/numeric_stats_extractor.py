from typing import Dict, List

import pandas as pd

from core.document_parser import URLData



class NumericStatsExtractor:
    def get_numeric_stats(self, docs: List[URLData]) -> Dict:
        df = pd.DataFrame(
            [
                {
                    "url": doc.url,
                    "word_count": doc.word_count,
                    "char_count": doc.char_count,
                    "subheading_count": doc.subheading_count,
                    "lists_count": doc.lists_count,
                    "tables_count": doc.tables_count,
                }
                for doc in docs
            ]
        )

        df = df.set_index("url")

        numeric_means = df.mean().to_dict()
        numeric_medians = df.median().to_dict()
        numeric_min = df.min().to_dict()
        numeric_max = df.max().to_dict()

        stats = {
            "mean": numeric_means,
            "median": numeric_medians,
            "min": numeric_min,
            "max": numeric_max,
            "distribution": {
                "word_count": df["word_count"].describe().to_dict(),
                "subheading_count": df["subheading_count"].describe().to_dict(),
            },
        }
        return stats
