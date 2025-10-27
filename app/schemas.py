from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import ContentType, Language

class ContentBase(BaseModel):
    content_type: ContentType
    language: Language
    title: str
    header: Optional[str] = None
    summary: str
    poster_url: Optional[str] = None
    content_html: str
    audio_url: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    content_type: Optional[ContentType] = None
    language: Optional[Language] = None
    title: Optional[str] = None
    header: Optional[str] = None
    summary: Optional[str] = None
    poster_url: Optional[str] = None
    content_html: Optional[str] = None
    audio_url: Optional[str] = None

class ContentResponse(ContentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
