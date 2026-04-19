from fastapi import HTTPException, status
from typing import Dict, List

from logger_config import get_logger

from backend.repositories import (
    ConversationRepository,
    MessageRepository,
    PlatformRepository,
    StatsRepository,
    UserRepository,
)
from backend.schemas import PlatformCreate, PlatformDTO, UserDTO

logger = get_logger(__name__)


class AdminService:
    def __init__(
        self,
        user_repository: UserRepository,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        platform_repository: PlatformRepository,
        stats_repository: StatsRepository,
    ):
        self.user_repository = user_repository
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.platform_repository = platform_repository
        self.stats_repository = stats_repository

    def ensure_admin(self, current_user: Dict) -> None:
        if not current_user.get("is_admin"):
            logger.error("[admin_service.py][ensure_admin] End status=error reason=forbidden user_id=%s", current_user.get("id"))
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can perform this action",
            )

    def get_all_users(self, current_user: Dict) -> List[UserDTO]:
        logger.info("[admin_service.py][get_all_users] Start business=list users")
        try:
            self.ensure_admin(current_user)
            users = self.user_repository.list_all()
            result = [
                UserDTO(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    full_name=user.full_name,
                    is_admin=user.is_admin,
                    created_at=user.created_at,
                )
                for user in users
            ]
            logger.info("[admin_service.py][get_all_users] End status=success count=%s", len(result))
            return result
        except HTTPException:
            raise
        except Exception:
            logger.exception("[admin_service.py][get_all_users] End status=error")
            raise

    def delete_user(self, user_id: str, current_user: Dict) -> None:
        logger.info("[admin_service.py][delete_user] Start business=delete user id=%s", user_id)
        try:
            self.ensure_admin(current_user)

            if user_id == current_user["id"]:
                logger.error("[admin_service.py][delete_user] End status=error reason=self_delete user_id=%s", user_id)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete your own account")

            conversation_ids = self.conversation_repository.list_ids_by_user(user_id)
            for conversation_id in conversation_ids:
                self.message_repository.delete_by_conversation(conversation_id)
            self.conversation_repository.delete_by_user(user_id)

            deleted = self.user_repository.delete_by_id(user_id)
            if not deleted:
                logger.error("[admin_service.py][delete_user] End status=error reason=not_found user_id=%s", user_id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            logger.info("[admin_service.py][delete_user] End status=success user_id=%s", user_id)
        except HTTPException:
            raise
        except Exception:
            logger.exception("[admin_service.py][delete_user] End status=error user_id=%s", user_id)
            raise

    def get_stats(self, current_user: Dict) -> Dict[str, int]:
        logger.info("[admin_service.py][get_stats] Start business=get system stats")
        try:
            self.ensure_admin(current_user)
            result = self.stats_repository.get_counts()
            logger.info("[admin_service.py][get_stats] End status=success")
            return result
        except HTTPException:
            raise
        except Exception:
            logger.exception("[admin_service.py][get_stats] End status=error")
            raise

    def get_platforms(self, current_user: Dict) -> List[PlatformDTO]:
        logger.info("[admin_service.py][get_platforms] Start business=list platforms")
        try:
            self.ensure_admin(current_user)
            platforms = self.platform_repository.list_all()
            result = [PlatformDTO(**platform.__dict__) for platform in platforms]
            logger.info("[admin_service.py][get_platforms] End status=success count=%s", len(result))
            return result
        except HTTPException:
            raise
        except Exception:
            logger.exception("[admin_service.py][get_platforms] End status=error")
            raise

    def create_platform(self, payload: PlatformCreate, current_user: Dict) -> PlatformDTO:
        logger.info("[admin_service.py][create_platform] Start business=create platform name=%s", payload.name)
        try:
            self.ensure_admin(current_user)
            platform = self.platform_repository.create(name=payload.name, url=payload.url, status=payload.status)
            logger.info("[admin_service.py][create_platform] End status=success platform_id=%s", platform.id)
            return PlatformDTO(**platform.__dict__)
        except HTTPException:
            raise
        except Exception:
            logger.exception("[admin_service.py][create_platform] End status=error name=%s", payload.name)
            raise

    def delete_platform(self, platform_id: str, current_user: Dict) -> None:
        logger.info("[admin_service.py][delete_platform] Start business=delete platform id=%s", platform_id)
        try:
            self.ensure_admin(current_user)
            deleted = self.platform_repository.delete_by_id(platform_id)
            if not deleted:
                logger.error("[admin_service.py][delete_platform] End status=error reason=not_found platform_id=%s", platform_id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform not found")

            logger.info("[admin_service.py][delete_platform] End status=success platform_id=%s", platform_id)
        except HTTPException:
            raise
        except Exception:
            logger.exception("[admin_service.py][delete_platform] End status=error platform_id=%s", platform_id)
            raise
