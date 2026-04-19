"""Compatibility wrapper for new db layer."""

from logger_config import get_logger

from backend.db import get_db, init_database
from backend.helpers import hash_password
from backend.repositories import ProductRepository

logger = get_logger(__name__)


def save_products(products: list) -> int:
    """Compatibility wrapper: delegate product persistence to repository layer."""
    logger.info("[database.py][save_products] Start business=save products count=%s", len(products))
    try:
        inserted = ProductRepository().insert_or_ignore_many(products)
        logger.info("[database.py][save_products] End status=success inserted=%s", inserted)
        return inserted
    except Exception:
        logger.exception("[database.py][save_products] End status=error")
        raise


__all__ = ["get_db", "init_database", "hash_password", "save_products"]
