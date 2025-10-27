from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ContentType(enum.Enum):
    STORY = "story"
    MANTRA = "mantra"
    AARTI = "aarti"

class Language(enum.Enum):
    HINDI = "hindi"
    ENGLISH = "english"

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    reference_id = Column(String(100), nullable=True, index=True)  # Links same content in different languages
    content_type = Column(Enum(ContentType), nullable=False, index=True)
    language = Column(Enum(Language), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    title_en = Column(String(255), nullable=True, index=True)  # English title (optional)
    header = Column(String(500), nullable=True)
    summary = Column(Text, nullable=False)
    summary_en = Column(Text, nullable=True)  # English summary (optional)
    poster_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)  # Banner for content page
    content_html = Column(Text, nullable=False)
    content_html_en = Column(Text, nullable=True)  # English content (optional)
    audio_url = Column(String(500), nullable=True)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Content {self.content_type.value}: {self.title}>"

