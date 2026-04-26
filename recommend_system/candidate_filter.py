from logger_config import get_logger

from .models import RecommendationResult, UserInteraction


log = get_logger(__name__)


class DefaultCandidateFilter:
    """Filter seen items and return highest scoring recommendations."""

    def select(
        self,
        scores: dict[str, float],
        interactions: list[UserInteraction],
        top_k: int,
        min_score: float,
    ) -> list[RecommendationResult]:
        if top_k <= 0:
            log.error("[DefaultCandidateFilter][select] Invalid top_k=%d", top_k)
            raise ValueError("top_k must be > 0")

        seen_item_ids = {interaction.item_id for interaction in interactions}

        log.info(
            "[DefaultCandidateFilter][select] Start scores=%d seen=%d top_k=%d min_score=%.4f",
            len(scores),
            len(seen_item_ids),
            top_k,
            min_score,
        )

        filtered = [
            (item_id, score)
            for item_id, score in scores.items()
            if item_id not in seen_item_ids and score >= min_score
        ]
        filtered.sort(key=lambda record: record[1], reverse=True)

        selected = filtered[:top_k]
        results = [
            RecommendationResult(
                item_id=item_id,
                score=score,
                reason="High content similarity with user profile",
            )
            for item_id, score in selected
        ]

        log.info(
            "[DefaultCandidateFilter][select] Done recommended=%d",
            len(results),
        )
        return results
