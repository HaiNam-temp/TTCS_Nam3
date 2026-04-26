from logger_config import get_logger

from .types import SparseVector
from .vector_utils import cosine_similarity


log = get_logger(__name__)


class CosineSimilarityScorer:
    """Score each item by cosine similarity to the user profile vector."""

    def score(
        self,
        user_vector: SparseVector,
        item_vectors: dict[str, SparseVector],
    ) -> dict[str, float]:
        if not user_vector:
            log.error("[CosineSimilarityScorer][score] Empty user_vector")
            raise ValueError("user_vector must not be empty")

        log.info(
            "[CosineSimilarityScorer][score] Start scoring items=%d",
            len(item_vectors),
        )

        scored = {
            item_id: cosine_similarity(user_vector, item_vector)
            for item_id, item_vector in item_vectors.items()
        }

        log.info("[CosineSimilarityScorer][score] Done")
        return scored
