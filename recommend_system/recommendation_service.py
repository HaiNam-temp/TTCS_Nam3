from logger_config import get_logger

from .candidate_filter import DefaultCandidateFilter
from .cosine_scorer import CosineSimilarityScorer
from .models import ItemContent, RecommendationResult, UserInteraction
from .tfidf_feature_extractor import TfidfFeatureExtractor
from .user_profile_builder import WeightedUserProfileBuilder


log = get_logger(__name__)


class ContentBasedRecommendationService:
    """Main orchestration service for content-based recommendations."""

    def __init__(self) -> None:
        self._feature_extractor = TfidfFeatureExtractor()
        self._user_profile_builder = WeightedUserProfileBuilder()
        self._scorer = CosineSimilarityScorer()
        self._candidate_filter = DefaultCandidateFilter()

    def recommend(
        self,
        items: list[ItemContent],
        interactions: list[UserInteraction],
        top_k: int = 10,
        min_score: float = 0.0,
    ) -> list[RecommendationResult]:
        """Return top-k content-based recommendations.

        Input:
        - items: all candidate items with textual content
        - interactions: user interaction history
        - top_k: number of final recommendations
        - min_score: minimum cosine score threshold

        Output:
        - list of RecommendationResult sorted by score descending
        """
        log.info(
            "[ContentBasedRecommendationService][recommend] Start items=%d interactions=%d top_k=%d",
            len(items),
            len(interactions),
            top_k,
        )

        try:
            item_vectors = self._feature_extractor.fit_transform(items)
            user_vector = self._user_profile_builder.build_profile(interactions, item_vectors)
            scores = self._scorer.score(user_vector, item_vectors)
            results = self._candidate_filter.select(
                scores=scores,
                interactions=interactions,
                top_k=top_k,
                min_score=min_score,
            )
            log.info(
                "[ContentBasedRecommendationService][recommend] Done results=%d",
                len(results),
            )
            return results
        except Exception as exc:
            log.error(
                "[ContentBasedRecommendationService][recommend] Failed: %s",
                str(exc),
                exc_info=True,
            )
            raise
