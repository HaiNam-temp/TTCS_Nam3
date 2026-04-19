"""Auth helpers."""
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

try:
    from logger_config import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

from .configs import active_tokens
from .helpers import hash_password, verify_password
from .repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_repository = UserRepository()



def create_access_token(user_id: str) -> str:
    """Create simple access token"""
    # Generate random token
    token = str(uuid.uuid4()) + str(uuid.uuid4()).replace("-", "")
    # Set expiration (24 hours)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    # Store in memory
    active_tokens[token] = {
        "user_id": user_id,
        "expires_at": expires_at
    }
    return token

def verify_token(token: str) -> Optional[str]:
    """Verify token and return user_id if valid"""
    if token not in active_tokens:
        return None
    
    token_data = active_tokens[token]
    # Check if expired
    if datetime.utcnow() > token_data["expires_at"]:
        del active_tokens[token]
        return None
    
    return token_data["user_id"]

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """Get current user from token"""
    logger.info("[auth.py][get_current_user] Start business=resolve current user from token")
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user_id = verify_token(token)
        if not user_id:
            logger.error("[auth.py][get_current_user] End status=error reason=invalid_token")
            raise credentials_exception

        user = user_repository.find_by_id(user_id)
        if user is None:
            logger.error("[auth.py][get_current_user] End status=error reason=user_not_found user_id=%s", user_id)
            raise credentials_exception

        logger.info("[auth.py][get_current_user] End status=success user_id=%s", user.id)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_admin": user.is_admin,
            "created_at": user.created_at,
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("[auth.py][get_current_user] End status=error")
        raise
