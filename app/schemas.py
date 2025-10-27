from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import ContentType, Language

class ContentBase(BaseModel):
    content_type: ContentType
    language: Language
    title: str
    title_en: Optional[str] = None
    header: Optional[str] = None
    summary: str
    summary_en: Optional[str] = None
    poster_url: Optional[str] = None
    banner_url: Optional[str] = None
    content_html: str
    content_html_en: Optional[str] = None
    audio_url: Optional[str] = None
    tags: Optional[str] = None
    reference_id: Optional[str] = None

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    content_type: Optional[ContentType] = None
    language: Optional[Language] = None
    title: Optional[str] = None
    title_en: Optional[str] = None
    header: Optional[str] = None
    summary: Optional[str] = None
    summary_en: Optional[str] = None
    poster_url: Optional[str] = None
    banner_url: Optional[str] = None
    content_html: Optional[str] = None
    content_html_en: Optional[str] = None
    audio_url: Optional[str] = None
    tags: Optional[str] = None
    reference_id: Optional[str] = None

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
