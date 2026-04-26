from logger_config import get_logger

from .models import UserInteraction
from .types import SparseVector
from .vector_utils import add_scaled, normalize


log = get_logger(__name__)


class WeightedUserProfileBuilder:
    """Create a user vector by weighted sum of interacted item vectors."""

    def build_profile(
        self,
        interactions: list[UserInteraction],
        item_vectors: dict[str, SparseVector],
    ) -> SparseVector:
        if not interactions:
            log.error("[WeightedUserProfileBuilder][build_profile] Empty interaction list")
            raise ValueError("interactions must not be empty")

        log.info(
            "[WeightedUserProfileBuilder][build_profile] Start interactions=%d",
            len(interactions),
        )

        profile: SparseVector = {}
        total_weight = 0.0

        for interaction in interactions:
            item_vector = item_vectors.get(interaction.item_id)
            if not item_vector:
                continue

            safe_weight = max(0.0, float(interaction.weight))
            profile = add_scaled(profile, item_vector, safe_weight)
            total_weight += safe_weight

        if total_weight == 0.0 or not profile:
            log.error("[WeightedUserProfileBuilder][build_profile] No valid vectors for interactions")
            raise ValueError("unable to build profile from interactions")

        averaged = {key: value / total_weight for key, value in profile.items()}
        normalized_profile = normalize(averaged)

        log.info(
            "[WeightedUserProfileBuilder][build_profile] Done profile_features=%d",
            len(normalized_profile),
        )
        return normalized_profile
