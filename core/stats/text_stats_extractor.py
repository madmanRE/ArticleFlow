import re
from typing import Dict, List

import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from core.document_parser import URLData

STOPWORDS = stopwords.words("russian") + stopwords.words("english")


class TextStatExtractor:
    def _clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-zа-яё0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def get_text_stats(self, docs: List[URLData]) -> Dict:
        texts = [self._clean_text(doc.text) for doc in docs]

        word_vectorizer = CountVectorizer(
            stop_words=STOPWORDS, ngram_range=(1, 1), max_features=2000
        )
        word_matrix = word_vectorizer.fit_transform(texts)
        word_freq = np.asarray(word_matrix.sum(axis=0)).ravel()
        top_words = sorted(
            zip(word_vectorizer.get_feature_names_out(), word_freq),
            key=lambda x: x[1],
            reverse=True,
        )[:30]

        bigram_vectorizer = CountVectorizer(
            stop_words=STOPWORDS, ngram_range=(2, 2), max_features=1000
        )
        bigram_matrix = bigram_vectorizer.fit_transform(texts)
        bigram_freq = np.asarray(bigram_matrix.sum(axis=0)).ravel()
        top_bigrams = sorted(
            zip(bigram_vectorizer.get_feature_names_out(), bigram_freq),
            key=lambda x: x[1],
            reverse=True,
        )[:20]

        trigram_vectorizer = CountVectorizer(
            stop_words=STOPWORDS, ngram_range=(3, 3), max_features=500
        )
        trigram_matrix = trigram_vectorizer.fit_transform(texts)
        trigram_freq = np.asarray(trigram_matrix.sum(axis=0)).ravel()
        top_trigrams = sorted(
            zip(trigram_vectorizer.get_feature_names_out(), trigram_freq),
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        tfidf = TfidfVectorizer(stop_words=STOPWORDS, max_features=1000)
        tfidf_matrix = tfidf.fit_transform(texts)
        tfidf_scores = np.asarray(tfidf_matrix.mean(axis=0)).ravel()
        top_tfidf = sorted(
            zip(tfidf.get_feature_names_out(), tfidf_scores),
            key=lambda x: x[1],
            reverse=True,
        )[:20]

        return {
            "top_words": top_words,
            "top_phrases_2": top_bigrams,
            "top_phrases_3": top_trigrams,
            "top_tfidf": top_tfidf,
            "total_unique_words": len(word_vectorizer.vocabulary_),
            "total_unique_phrases": len(bigram_vectorizer.vocabulary_)
                                    + len(trigram_vectorizer.vocabulary_),
        }
