"""Content-based recommendation system package.

Simple and clean building blocks for a content-based recommender.
"""

from .candidate_filter import DefaultCandidateFilter
from .cosine_scorer import CosineSimilarityScorer
from .models import ItemContent, RecommendationResult, UserInteraction
from .recommendation_service import ContentBasedRecommendationService
from .tfidf_feature_extractor import TfidfFeatureExtractor
from .user_profile_builder import WeightedUserProfileBuilder

__all__ = [
    "ContentBasedRecommendationService",
    "DefaultCandidateFilter",
    "CosineSimilarityScorer",
    "ItemContent",
    "RecommendationResult",
    "TfidfFeatureExtractor",
    "UserInteraction",
    "WeightedUserProfileBuilder",
]
