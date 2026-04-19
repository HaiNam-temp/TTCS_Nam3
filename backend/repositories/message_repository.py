from datetime import datetime
from typing import List
import uuid

from logger_config import get_logger

from backend.models import MessageModel
from backend.repositories.base import db_cursor

logger = get_logger(__name__)


class MessageRepository:
    def create(self, conversation_id: str, role: str, content: str) -> MessageModel:
        logger.info("[message_repository.py][create] Insert message role=%s conversation_id=%s", role, conversation_id)
        message = MessageModel(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.utcnow().isoformat(),
        )
        with db_cursor() as (_, cursor):
            cursor.execute(
                """
                INSERT INTO messages (id, conversation_id, role, content, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (message.id, message.conversation_id, message.role, message.content, message.created_at),
            )
        return message

    def list_by_conversation(self, conversation_id: str) -> List[MessageModel]:
        logger.info("[message_repository.py][list_by_conversation] Query messages conversation_id=%s", conversation_id)
        with db_cursor() as (_, cursor):
            cursor.execute(
                "SELECT * FROM messages WHERE conversation_id = %s ORDER BY created_at ASC",
                (conversation_id,),
            )
            rows = cursor.fetchall()
        return [
            MessageModel(
                id=row["id"],
                conversation_id=row["conversation_id"],
                role=row["role"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def delete_by_conversation(self, conversation_id: str) -> int:
        logger.info("[message_repository.py][delete_by_conversation] Delete messages conversation_id=%s", conversation_id)
        with db_cursor() as (_, cursor):
            cursor.execute("DELETE FROM messages WHERE conversation_id = %s", (conversation_id,))
            return cursor.rowcount
