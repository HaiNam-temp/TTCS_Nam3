"""Admin routes layer (HTTP only)."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List

try:
    from logger_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

from ..auth import get_current_user
from ..schemas import PlatformCreate, PlatformDTO, UserDTO
from ..services.container import admin_service

router = APIRouter()

@router.get("/admin/users/", response_model=List[UserDTO])
async def get_all_users(current_user: Dict = Depends(get_current_user)):
    """Get all users (admin only)"""
    logger.info("[admin_routes.py][get_all_users] Start route call")
    try:
        result = admin_service.get_all_users(current_user)
        logger.info("[admin_routes.py][get_all_users] End status=success count=%s", len(result))
        return result
    except HTTPException:
        logger.error("[admin_routes.py][get_all_users] End status=error type=http_exception")
        raise
    except Exception:
        logger.exception("[admin_routes.py][get_all_users] End status=error")
        raise

@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a user (admin only)"""
    logger.info("[admin_routes.py][delete_user] Start route call user_id=%s", user_id)
    try:
        admin_service.delete_user(user_id, current_user)
        logger.info("[admin_routes.py][delete_user] End status=success user_id=%s", user_id)
        return None
    except HTTPException:
        logger.error("[admin_routes.py][delete_user] End status=error type=http_exception user_id=%s", user_id)
        raise
    except Exception:
        logger.exception("[admin_routes.py][delete_user] End status=error user_id=%s", user_id)
        raise

@router.get("/admin/stats")
async def get_stats(current_user: Dict = Depends(get_current_user)):
    """Get system statistics (admin only)"""
    logger.info("[admin_routes.py][get_stats] Start route call")
    try:
        result = admin_service.get_stats(current_user)
        logger.info("[admin_routes.py][get_stats] End status=success")
        return result
    except HTTPException:
        logger.error("[admin_routes.py][get_stats] End status=error type=http_exception")
        raise
    except Exception:
        logger.exception("[admin_routes.py][get_stats] End status=error")
        raise

@router.get("/platforms/", response_model=List[PlatformDTO])
async def get_platforms(current_user: Dict = Depends(get_current_user)):
    """Get all platforms (admin feature)"""
    logger.info("[admin_routes.py][get_platforms] Start route call")
    try:
        result = admin_service.get_platforms(current_user)
        logger.info("[admin_routes.py][get_platforms] End status=success count=%s", len(result))
        return result
    except HTTPException:
        logger.error("[admin_routes.py][get_platforms] End status=error type=http_exception")
        raise
    except Exception:
        logger.exception("[admin_routes.py][get_platforms] End status=error")
        raise

@router.post("/platforms/", response_model=PlatformDTO, status_code=status.HTTP_201_CREATED)
async def create_platform(
    platform: PlatformCreate,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new platform (admin only)"""
    logger.info("[admin_routes.py][create_platform] Start route call name=%s", platform.name)
    try:
        result = admin_service.create_platform(platform, current_user)
        logger.info("[admin_routes.py][create_platform] End status=success platform_id=%s", result.id)
        return result
    except HTTPException:
        logger.error("[admin_routes.py][create_platform] End status=error type=http_exception name=%s", platform.name)
        raise
    except Exception:
        logger.exception("[admin_routes.py][create_platform] End status=error name=%s", platform.name)
        raise

@router.delete("/platforms/{platform_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_platform(
    platform_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a platform (admin only)"""
    logger.info("[admin_routes.py][delete_platform] Start route call platform_id=%s", platform_id)
    try:
        admin_service.delete_platform(platform_id, current_user)
        logger.info("[admin_routes.py][delete_platform] End status=success platform_id=%s", platform_id)
        return None
    except HTTPException:
        logger.error("[admin_routes.py][delete_platform] End status=error type=http_exception platform_id=%s", platform_id)
        raise
    except Exception:
        logger.exception("[admin_routes.py][delete_platform] End status=error platform_id=%s", platform_id)
        raise
