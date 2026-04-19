from typing import Dict

from logger_config import get_logger

from backend.repositories.base import db_cursor

logger = get_logger(__name__)


class StatsRepository:
    def get_counts(self) -> Dict[str, int]:
        logger.info("[stats_repository.py][get_counts] Query system counters")
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT COUNT(*) as count FROM users")
            total_users = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM conversations")
            total_conversations = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM messages")
            total_messages = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) as count FROM platforms")
            total_platforms = cursor.fetchone()["count"]

        return {
            "total_users": total_users,
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "total_platforms": total_platforms,
        }
