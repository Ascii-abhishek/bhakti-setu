from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.models import Content, ContentType, Language
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_all_contents(
    db: Session,
    content_type: Optional[ContentType] = None,
    language: Optional[Language] = None,
    skip: int = 0,
    limit: int = 100,
    shuffle: bool = False
) -> List[Content]:
    """Get all contents with optional filtering"""
    query = db.query(Content)
    
    if content_type:
        query = query.filter(Content.content_type == content_type)
    
    if language:
        query = query.filter(Content.language == language)
    
    if shuffle:
        query = query.order_by(func.random())
    else:
        query = query.order_by(Content.created_at.desc())
    
    return query.offset(skip).limit(limit).all()

def get_content_by_id(db: Session, content_id: int) -> Optional[Content]:
    """Get a specific content by ID"""
    return db.query(Content).filter(Content.id == content_id).first()

def search_contents(
    db: Session,
    query: str,
    content_type: Optional[ContentType] = None,
    language: Optional[Language] = None
) -> List[Content]:
    """Search contents by title or summary"""
    search_query = db.query(Content).filter(
        (Content.title.ilike(f"%{query}%")) | 
        (Content.summary.ilike(f"%{query}%"))
    )
    
    if content_type:
        search_query = search_query.filter(Content.content_type == content_type)
    
    if language:
        search_query = search_query.filter(Content.language == language)
    
    return search_query.all()

def create_content(db: Session, content_data: dict) -> Content:
    """Create a new content"""
    content = Content(**content_data)
    db.add(content)
    db.commit()
    db.refresh(content)
    return content

def update_content(db: Session, content_id: int, content_data: dict) -> Optional[Content]:
    """Update an existing content"""
    content = db.query(Content).filter(Content.id == content_id).first()
    if content:
        for key, value in content_data.items():
            setattr(content, key, value)
        db.commit()
        db.refresh(content)
    return content

def delete_content(db: Session, content_id: int) -> bool:
    """Delete a content"""
    content = db.query(Content).filter(Content.id == content_id).first()
    if content:
        db.delete(content)
        db.commit()
        return True
    return False

def get_random_content(db: Session, content_type: Optional[ContentType] = None) -> Optional[Content]:
    """Get a random content"""
    query = db.query(Content)
    if content_type:
        query = query.filter(Content.content_type == content_type)
    return query.order_by(func.random()).first()
