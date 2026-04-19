from fastapi import HTTPException, status

from logger_config import get_logger

from backend.auth import create_access_token, hash_password, verify_password
from backend.repositories import UserRepository
from backend.schemas import Token, UserCreate, UserDTO

logger = get_logger(__name__)


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login_user(self, username: str, password: str) -> Token:
        logger.info("[auth_service.py][login_user] Start business=authenticate username=%s", username)
        try:
            user = self.user_repository.find_by_username(username)
            if not user or not verify_password(password, user.password_hash):
                logger.error("[auth_service.py][login_user] End status=error reason=invalid_credentials username=%s", username)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token = create_access_token(user.id)
            logger.info("[auth_service.py][login_user] End status=success user_id=%s", user.id)
            return Token(access_token=token, token_type="bearer")
        except HTTPException:
            raise
        except Exception:
            logger.exception("[auth_service.py][login_user] End status=error username=%s", username)
            raise

    def register_user(self, user_data: UserCreate) -> UserDTO:
        logger.info("[auth_service.py][register_user] Start business=register username=%s", user_data.username)
        try:
            if user_data.username.lower() == "admin":
                logger.error("[auth_service.py][register_user] End status=error reason=forbidden_username username=%s", user_data.username)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Khong the dang ky voi username 'admin'. Tai khoan admin da duoc tao san.",
                )

            if self.user_repository.exists_by_username_or_email(user_data.username, str(user_data.email)):
                logger.error("[auth_service.py][register_user] End status=error reason=duplicate_user username=%s", user_data.username)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username hoac email da duoc dang ky",
                )

            user = self.user_repository.insert_user(
                username=user_data.username,
                email=str(user_data.email),
                password_hash=hash_password(user_data.password),
                full_name=user_data.full_name,
                is_admin=False,
            )
            logger.info("[auth_service.py][register_user] End status=success user_id=%s", user.id)
            return UserDTO(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                is_admin=user.is_admin,
                created_at=user.created_at,
            )
        except HTTPException:
            raise
        except Exception:
            logger.exception("[auth_service.py][register_user] End status=error username=%s", user_data.username)
            raise

    @staticmethod
    def to_user_dto(user_model) -> UserDTO:
        return UserDTO(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            full_name=user_model.full_name,
            is_admin=user_model.is_admin,
            created_at=user_model.created_at,
        )
