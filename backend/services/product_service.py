from fastapi import HTTPException
from typing import List, Optional

from logger_config import get_logger

from backend.repositories import ProductRepository
from backend.schemas import ProductDTO

logger = get_logger(__name__)


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def list_products(self, q: Optional[str], limit: int, offset: int) -> List[ProductDTO]:
        logger.info("[product_service.py][list_products] Start business=list products")
        try:
            items = self.product_repository.list_products(q=q, limit=limit, offset=offset)
            result = [
                ProductDTO(
                    id=item.id,
                    name=item.name,
                    price=item.price,
                    url=item.url,
                    image=item.image,
                    rating=item.rating,
                    review_count=item.review_count,
                    metadata=item.metadata,
                    created_at=item.created_at,
                )
                for item in items
            ]
            logger.info("[product_service.py][list_products] End status=success count=%s", len(result))
            return result
        except Exception:
            logger.exception("[product_service.py][list_products] End status=error")
            raise

    def get_product(self, product_id: str) -> ProductDTO:
        logger.info("[product_service.py][get_product] Start business=get product id=%s", product_id)
        try:
            item = self.product_repository.get_by_id(product_id)
            if not item:
                logger.error("[product_service.py][get_product] End status=error reason=not_found product_id=%s", product_id)
                raise HTTPException(status_code=404, detail="Product not found")

            logger.info("[product_service.py][get_product] End status=success product_id=%s", product_id)
            return ProductDTO(
                id=item.id,
                name=item.name,
                price=item.price,
                url=item.url,
                image=item.image,
                rating=item.rating,
                review_count=item.review_count,
                metadata=item.metadata,
                created_at=item.created_at,
            )
        except HTTPException:
            raise
        except Exception:
            logger.exception("[product_service.py][get_product] End status=error product_id=%s", product_id)
            raise

    def save_crawled_products(self, products: list) -> int:
        logger.info("[product_service.py][save_crawled_products] Start business=save crawled products")
        try:
            inserted = self.product_repository.insert_or_ignore_many(products)
            logger.info("[product_service.py][save_crawled_products] End status=success inserted=%s", inserted)
            return inserted
        except Exception:
            logger.exception("[product_service.py][save_crawled_products] End status=error")
            raise
