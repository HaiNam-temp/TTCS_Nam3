"""Product routes - expose products stored in the SQLite DB

Endpoints:
- GET /products/        -> list products, optional q (search), limit, offset
- GET /products/{id}    -> get single product by id

These are intentionally public (no auth) so the frontend can query persisted
crawl results. Keep implementations simple and use the existing `get_db()`
helper and `Product` Pydantic model for responses.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional

try:
    from logger_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

from ..schemas import ProductDTO
from ..services.container import product_service

router = APIRouter(prefix="/products")


@router.get("/", response_model=List[ProductDTO])
async def list_products(q: Optional[str] = Query(None), limit: int = 50, offset: int = 0):
    """List products stored in the database.

    Optional query `q` performs a simple LIKE search against name and url.
    """
    logger.info("[product_routes.py][list_products] Start route call")
    try:
        result = product_service.list_products(q=q, limit=limit, offset=offset)
        logger.info("[product_routes.py][list_products] End status=success count=%s", len(result))
        return result
    except HTTPException:
        logger.error("[product_routes.py][list_products] End status=error type=http_exception")
        raise
    except Exception:
        logger.exception("[product_routes.py][list_products] End status=error")
        raise


@router.get("/{product_id}", response_model=ProductDTO)
async def get_product(product_id: str):
    """Return a single product by ID."""
    logger.info("[product_routes.py][get_product] Start route call product_id=%s", product_id)
    try:
        result = product_service.get_product(product_id)
        logger.info("[product_routes.py][get_product] End status=success product_id=%s", product_id)
        return result
    except HTTPException:
        logger.error("[product_routes.py][get_product] End status=error type=http_exception product_id=%s", product_id)
        raise
    except Exception:
        logger.exception("[product_routes.py][get_product] End status=error product_id=%s", product_id)
        raise
