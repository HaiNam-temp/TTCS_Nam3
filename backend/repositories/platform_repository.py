from datetime import datetime
from typing import List
import uuid

from logger_config import get_logger

from backend.models import PlatformModel
from backend.repositories.base import db_cursor

logger = get_logger(__name__)


class PlatformRepository:
    def list_all(self) -> List[PlatformModel]:
        logger.info("[platform_repository.py][list_all] Query platforms")
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT * FROM platforms ORDER BY created_at DESC")
            rows = cursor.fetchall()
        return [self._to_model(row) for row in rows]

    def create(self, name: str, url: str, status: str) -> PlatformModel:
        logger.info("[platform_repository.py][create] Insert platform name=%s", name)
        platform = PlatformModel(
            id=str(uuid.uuid4()),
            name=name,
            url=url,
            status=status,
            created_at=datetime.utcnow().isoformat(),
        )
        with db_cursor() as (_, cursor):
            cursor.execute(
                """
                INSERT INTO platforms (id, name, url, status, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (platform.id, platform.name, platform.url, platform.status, platform.created_at),
            )
        return platform

    def delete_by_id(self, platform_id: str) -> bool:
        logger.info("[platform_repository.py][delete_by_id] Delete platform id=%s", platform_id)
        with db_cursor() as (_, cursor):
            cursor.execute("DELETE FROM platforms WHERE id = %s", (platform_id,))
            return cursor.rowcount > 0

    @staticmethod
    def _to_model(row) -> PlatformModel:
        return PlatformModel(
            id=row["id"],
            name=row["name"],
            url=row["url"],
            status=row["status"],
            created_at=row["created_at"],
        )
