from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserDTO(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    is_admin: bool = False
    created_at: str


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"


class ConversationDTO(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str


class MessageCreate(BaseModel):
    content: str


class MessageDTO(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: str


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    message_id: str


class PlatformCreate(BaseModel):
    name: str
    url: str
    status: str = "active"


class PlatformDTO(BaseModel):
    id: str
    name: str
    url: str
    status: str
    created_at: str


class ProductCreate(BaseModel):
    name: str
    price: Optional[float] = None
    url: str
    image: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class ProductDTO(BaseModel):
    id: str
    name: str
    price: Optional[float] = None
    url: str
    image: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: str


class CrawlProductsRequest(BaseModel):
    query: str
    limit: int = 20


class CrawlSourceResult(BaseModel):
    source: str
    count: int
    error: Optional[str] = None


class CrawlProductsResponse(BaseModel):
    query: str
    total_products: int
    inserted_products: int
    elapsed_seconds: float
    sources: List[CrawlSourceResult]
