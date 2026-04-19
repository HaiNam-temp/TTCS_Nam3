from datetime import datetime
import uuid
from typing import Dict, List, Optional

from logger_config import get_logger

from backend.models import ProductModel
from backend.repositories.base import db_cursor, from_json, to_json

logger = get_logger(__name__)


class ProductRepository:
    def list_products(self, q: Optional[str], limit: int, offset: int) -> List[ProductModel]:
        logger.info("[product_repository.py][list_products] Run query list products q=%s limit=%s offset=%s", q, limit, offset)
        with db_cursor() as (_, cursor):
            if q:
                like = f"%{q}%"
                cursor.execute(
                    "SELECT * FROM products WHERE name ILIKE %s OR url ILIKE %s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                    (like, like, limit, offset),
                )
            else:
                cursor.execute(
                    "SELECT * FROM products ORDER BY created_at DESC LIMIT %s OFFSET %s",
                    (limit, offset),
                )
            rows = cursor.fetchall()
        return [self._to_model(row) for row in rows]

    def get_by_id(self, product_id: str) -> Optional[ProductModel]:
        logger.info("[product_repository.py][get_by_id] Run query product id=%s", product_id)
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            row = cursor.fetchone()
        return self._to_model(row) if row else None

    def insert_or_ignore_many(self, products: List[Dict]) -> int:
        logger.info("[product_repository.py][insert_or_ignore_many] Insert products size=%s", len(products))
        inserted = 0
        with db_cursor() as (_, cursor):
            for item in products:
                product_id = item.get("id") or str(uuid.uuid4())
                name = item.get("name") or item.get("title") or item.get("product_name") or ""
                url = item.get("url") or item.get("link") or ""
                if not name or not url:
                    continue
                cursor.execute(
                    """
                    INSERT INTO products
                    (id, name, price, url, image, rating, review_count, metadata, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s)
                    ON CONFLICT (url) DO NOTHING
                    """,
                    (
                        product_id,
                        name,
                        item.get("price"),
                        url,
                        item.get("image"),
                        self._to_float(item.get("rating")),
                        self._to_int(item.get("review_count")),
                        to_json(item.get("metadata")),
                        item.get("timestamp") or datetime.utcnow().isoformat(),
                    ),
                )
                if cursor.rowcount > 0:
                    inserted += 1
        return inserted

    @staticmethod
    def _to_model(row) -> ProductModel:
        return ProductModel(
            id=row["id"],
            name=row["name"],
            price=row["price"],
            url=row["url"],
            image=row["image"],
            rating=row["rating"],
            review_count=row["review_count"],
            metadata=from_json(row["metadata"]),
            created_at=row["created_at"],
        )

    @staticmethod
    def _to_float(value):
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            return None

    @staticmethod
    def _to_int(value):
        if value is None:
            return None
        try:
            return int(value)
        except Exception:
            return None
