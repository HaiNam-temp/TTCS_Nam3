"""Domain entities for backend model layer."""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class UserModel:
    id: str
    username: str
    email: str
    password_hash: str
    full_name: Optional[str]
    is_admin: bool
    created_at: str


@dataclass
class ConversationModel:
    id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str


@dataclass
class MessageModel:
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: str


@dataclass
class PlatformModel:
    id: str
    name: str
    url: str
    status: str
    created_at: str


@dataclass
class ProductModel:
    id: str
    name: str
    price: Optional[float]
    url: str
    image: Optional[str]
    rating: Optional[float]
    review_count: Optional[int]
    metadata: Optional[Dict[str, Any]]
    created_at: str
