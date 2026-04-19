from fastapi import APIRouter, Depends, HTTPException
from typing import Dict

from logger_config import get_logger

from ..auth import get_current_user
from ..schemas import CrawlProductsRequest, CrawlProductsResponse
from ..services.container import admin_service, crawl_service

logger = get_logger(__name__)
router = APIRouter()


@router.post("/admin/batch/crawl-products", response_model=CrawlProductsResponse)
async def crawl_products(payload: CrawlProductsRequest, current_user: Dict = Depends(get_current_user)):
	"""Admin endpoint to crawl products from all sources and persist to DB."""
	logger.info("[admin_batch_routes.py][crawl_products] Start route call query=%s", payload.query)
	try:
		admin_service.ensure_admin(current_user)
		result = crawl_service.crawl_and_store(payload.query, payload.limit)
		logger.info(
			"[admin_batch_routes.py][crawl_products] End status=success total_products=%s inserted=%s",
			result.total_products,
			result.inserted_products,
		)
		return result
	except HTTPException:
		logger.error("[admin_batch_routes.py][crawl_products] End status=error type=http_exception query=%s", payload.query)
		raise
	except Exception:
		logger.exception("[admin_batch_routes.py][crawl_products] End status=error query=%s", payload.query)
		raise
