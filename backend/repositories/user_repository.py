from datetime import datetime
from typing import List, Optional
import uuid

from logger_config import get_logger

from backend.models import UserModel
from backend.repositories.base import db_cursor

logger = get_logger(__name__)


class UserRepository:
    def find_by_username(self, username: str) -> Optional[UserModel]:
        logger.info("[user_repository.py][find_by_username] Run query users by username=%s", username)
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
        return self._to_model(row)

    def find_by_id(self, user_id: str) -> Optional[UserModel]:
        logger.info("[user_repository.py][find_by_id] Run query users by id=%s", user_id)
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
        return self._to_model(row)

    def exists_by_username_or_email(self, username: str, email: str) -> bool:
        logger.info("[user_repository.py][exists_by_username_or_email] Check duplicate username/email")
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            return cursor.fetchone() is not None

    def insert_user(self, username: str, email: str, password_hash: str, full_name: Optional[str], is_admin: bool = False) -> UserModel:
        logger.info("[user_repository.py][insert_user] Insert new user username=%s is_admin=%s", username, is_admin)
        user = UserModel(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            is_admin=is_admin,
            created_at=datetime.utcnow().isoformat(),
        )
        with db_cursor() as (_, cursor):
            cursor.execute(
                """
                INSERT INTO users (id, username, email, password_hash, full_name, is_admin, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user.id,
                    user.username,
                    user.email,
                    user.password_hash,
                    user.full_name,
                    bool(user.is_admin),
                    user.created_at,
                ),
            )
        return user

    def list_all(self) -> List[UserModel]:
        logger.info("[user_repository.py][list_all] Run query list users")
        with db_cursor() as (_, cursor):
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
            rows = cursor.fetchall()
        return [self._to_model(row) for row in rows if row]

    def delete_by_id(self, user_id: str) -> bool:
        logger.info("[user_repository.py][delete_by_id] Delete user id=%s", user_id)
        with db_cursor() as (_, cursor):
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            return cursor.rowcount > 0

    @staticmethod
    def _to_model(row) -> Optional[UserModel]:
        if not row:
            return None
        return UserModel(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
            full_name=row["full_name"],
            is_admin=bool(row["is_admin"]),
            created_at=row["created_at"],
        )
