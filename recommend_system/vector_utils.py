import math

from .types import SparseVector


def l2_norm(vector: SparseVector) -> float:
    """Compute L2 norm of a sparse vector."""
    return math.sqrt(sum(value * value for value in vector.values()))


def normalize(vector: SparseVector) -> SparseVector:
    """Return a normalized copy of the sparse vector."""
    norm = l2_norm(vector)
    if norm == 0.0:
        return {}
    return {key: value / norm for key, value in vector.items()}


def cosine_similarity(left: SparseVector, right: SparseVector) -> float:
    """Compute cosine similarity between two sparse vectors."""
    if not left or not right:
        return 0.0

    if len(left) <= len(right):
        dot = sum(value * right.get(key, 0.0) for key, value in left.items())
    else:
        dot = sum(value * left.get(key, 0.0) for key, value in right.items())

    left_norm = l2_norm(left)
    right_norm = l2_norm(right)
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def add_scaled(target: SparseVector, source: SparseVector, scale: float) -> SparseVector:
    """Add a scaled sparse vector into target and return a new vector."""
    if scale == 0.0 or not source:
        return dict(target)

    result = dict(target)
    for key, value in source.items():
        result[key] = result.get(key, 0.0) + (value * scale)
    return result
