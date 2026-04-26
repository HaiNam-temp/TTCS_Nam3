from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ItemContent:
    """Domain model representing an item and its textual content."""

    item_id: str
    title: str
    description: str = ""
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class UserInteraction:
    """Domain model for a user interaction with an item."""

    item_id: str
    weight: float = 1.0
    timestamp: float | None = None


@dataclass(frozen=True)
class RecommendationResult:
    """Output record of a recommendation run."""

    item_id: str
    score: float
    reason: str = ""
