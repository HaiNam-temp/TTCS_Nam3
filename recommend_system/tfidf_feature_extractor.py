from __future__ import annotations

import math

from logger_config import get_logger

from .models import ItemContent
from .text_preprocessor import tokenize
from .types import SparseVector
from .vector_utils import normalize


log = get_logger(__name__)


class TfidfFeatureExtractor:
    """Build TF-IDF item vectors from item content fields."""

    def __init__(self) -> None:
        self._idf: dict[str, float] = {}

    def fit_transform(self, items: list[ItemContent]) -> dict[str, SparseVector]:
        if not items:
            log.error("[TfidfFeatureExtractor][fit_transform] Empty item list")
            raise ValueError("items must not be empty")

        log.info(
            "[TfidfFeatureExtractor][fit_transform] Start building vectors for %d items",
            len(items),
        )

        tokenized_items: dict[str, list[str]] = {}
        document_frequency: dict[str, int] = {}

        for item in items:
            tokens = self._item_tokens(item)
            tokenized_items[item.item_id] = tokens

            for token in set(tokens):
                document_frequency[token] = document_frequency.get(token, 0) + 1

        total_docs = len(items)
        self._idf = {
            token: math.log((1 + total_docs) / (1 + doc_freq)) + 1.0
            for token, doc_freq in document_frequency.items()
        }

        item_vectors: dict[str, SparseVector] = {}
        for item_id, tokens in tokenized_items.items():
            if not tokens:
                item_vectors[item_id] = {}
                continue

            term_frequency: dict[str, float] = {}
            for token in tokens:
                term_frequency[token] = term_frequency.get(token, 0.0) + 1.0

            token_count = float(len(tokens))
            raw_vector = {
                token: (term_count / token_count) * self._idf.get(token, 0.0)
                for token, term_count in term_frequency.items()
            }
            item_vectors[item_id] = normalize(raw_vector)

        log.info(
            "[TfidfFeatureExtractor][fit_transform] Done vocabulary_size=%d",
            len(self._idf),
        )
        return item_vectors

    @staticmethod
    def _item_tokens(item: ItemContent) -> list[str]:
        # Merge text fields that represent item content.
        text_fields = [
            item.title,
            item.description,
            " ".join(item.categories),
            " ".join(item.tags),
        ]
        return tokenize(" ".join(text_fields))
