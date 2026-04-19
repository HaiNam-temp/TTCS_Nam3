from datetime import datetime
from typing import List, Optional
import uuid

from logger_config import get_logger

from backend.models import ConversationModel
from backend.repositories.base import db_cursor

logger = get_logger(__name__)


class ConversationRepository:
    def create(self, user_id: str, title: str) -> ConversationModel:
        logger.info("[conversation_repository.py][create] Insert conversation user_id=%s", user_id)
        now = datetime.utcnow().isoformat()
        conversation = ConversationModel(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            created_at=now,
            updated_at=now,
        )
        with db_cursor() as (_, cursor):
            cursor.execute(
                """
                INSERT INTO conversations (id, user_id, title, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (conversation.id, conversation.user_id, conversation.title, conversation.created_at, conversation.updated_at),
            )
        return conversation

    def list_by_user(self, user_id: str) -> List[ConversationModel]:
        logger.info("[conversation_repository.py][list_by_user] Query conversations user_id=%s", user_id)
        with db_cursor() as (_, cursor):
            cursor.execute(
                "SELECT * FROM conversations WHERE user_id = %s ORDER BY updated_at DESC",
                (user_id,),
            )
            rows = cursor.fetchall()
        return [self._to_model(row) for row in rows]

    def find_by_id_and_user(self, conversation_id: str, user_id: str) -> Optional[ConversationModel]:
        logger.info("[conversation_repository.py][find_by_id_and_user] Query conversation id=%s user_id=%s", conversation_id, user_id)
        with db_cursor() as (_, cursor):
            cursor.execute(
                "SELECT * FROM conversations WHERE id = %s AND user_id = %s",
                (conversation_id, user_id),
            )
            row = cursor.fetchone()
        return self._to_model(row) if row else None

    def list_ids_by_user(self, user_id: str) -> List[str]:
        logger.info("[conversation_repository.py][list_ids_by_user] Query conversation ids user_id=%s", user_id)
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT id FROM conversations WHERE user_id = %s", (user_id,))
            rows = cursor.fetchall()
        return [row["id"] for row in rows]

    def delete_by_id(self, conversation_id: str) -> bool:
        logger.info("[conversation_repository.py][delete_by_id] Delete conversation id=%s", conversation_id)
        with db_cursor() as (_, cursor):
            cursor.execute("DELETE FROM conversations WHERE id = %s", (conversation_id,))
            return cursor.rowcount > 0

    def delete_by_user(self, user_id: str) -> int:
        logger.info("[conversation_repository.py][delete_by_user] Delete conversations user_id=%s", user_id)
        with db_cursor() as (_, cursor):
            cursor.execute("DELETE FROM conversations WHERE user_id = %s", (user_id,))
            return cursor.rowcount

    def touch_updated_at(self, conversation_id: str, updated_at: str) -> None:
        logger.info("[conversation_repository.py][touch_updated_at] Update timestamp conversation id=%s", conversation_id)
        with db_cursor() as (_, cursor):
            cursor.execute(
                "UPDATE conversations SET updated_at = %s WHERE id = %s",
                (updated_at, conversation_id),
            )

    @staticmethod
    def _to_model(row) -> ConversationModel:
        return ConversationModel(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
