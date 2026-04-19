"""Authentication routes layer (HTTP only)."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict

try:
    from logger_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

from ..auth import get_current_user
from ..schemas import Token, UserCreate, UserDTO
from ..services.container import auth_service

router = APIRouter()

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint - returns access token."""
    try:
        logger.info("[auth_routes.py][login] Start business=login route username=%s", form_data.username)
        result = auth_service.login_user(form_data.username, form_data.password)
        logger.info("[auth_routes.py][login] End status=success username=%s", form_data.username)
        return result
    except HTTPException:
        logger.error("[auth_routes.py][login] End status=error type=http_exception username=%s", form_data.username)
        raise
    except Exception as e:
        logger.exception("[auth_routes.py][login] End status=error username=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/users/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """Register a new user."""
    logger.info("[auth_routes.py][register_user] Start business=register route username=%s", user.username)
    try:
        result = auth_service.register_user(user)
        logger.info("[auth_routes.py][register_user] End status=success username=%s", user.username)
        return result
    except HTTPException:
        logger.error("[auth_routes.py][register_user] End status=error type=http_exception username=%s", user.username)
        raise
    except Exception:
        logger.exception("[auth_routes.py][register_user] End status=error username=%s", user.username)
        raise

@router.get("/users/me", response_model=UserDTO)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user information."""
    logger.info("[auth_routes.py][get_current_user_info] Start business=get current user")
    try:
        result = UserDTO(
            id=current_user["id"],
            username=current_user["username"],
            email=current_user["email"],
            full_name=current_user["full_name"],
            is_admin=bool(current_user["is_admin"]),
            created_at=current_user["created_at"]
        )
        logger.info("[auth_routes.py][get_current_user_info] End status=success user_id=%s", current_user["id"])
        return result
    except Exception:
        logger.exception("[auth_routes.py][get_current_user_info] End status=error user_id=%s", current_user.get("id"))
        raise
