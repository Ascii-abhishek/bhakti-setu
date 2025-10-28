from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import ContentType


class ContentBase(BaseModel):
    content_type: ContentType
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
    """Schema for creating content - uses ContentBase directly"""
    pass


class ContentUpdate(BaseModel):
    content_type: Optional[ContentType] = None
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
