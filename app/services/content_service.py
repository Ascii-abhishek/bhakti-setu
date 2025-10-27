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
    """Search contents by title, summary, tags, or content with relevance scoring"""
    search_term = f"%{query}%"
    
    # Simple search across all fields
    search_query = db.query(Content).filter(
        (Content.title.ilike(search_term)) | 
        (Content.title_en.ilike(search_term)) |
        (Content.summary.ilike(search_term)) |
        (Content.summary_en.ilike(search_term)) |
        (Content.tags.ilike(search_term)) |
        (Content.content_html.ilike(search_term)) |
        (Content.content_html_en.ilike(search_term))
    )
    
    if content_type:
        search_query = search_query.filter(Content.content_type == content_type)
    
    if language:
        search_query = search_query.filter(Content.language == language)
    
    # Get all matching results
    results = search_query.all()
    
    # Sort by relevance in Python (more reliable)
    def calculate_relevance(content):
        score = 0
        query_lower = query.lower()
        
        # Title matches (highest priority)
        if content.title and query_lower in content.title.lower():
            score += 10
        if content.title_en and query_lower in content.title_en.lower():
            score += 10
            
        # Tag matches (very high priority)
        if content.tags and query_lower in content.tags.lower():
            score += 8
            
        # Summary matches (medium priority)
        if content.summary and query_lower in content.summary.lower():
            score += 5
        if content.summary_en and query_lower in content.summary_en.lower():
            score += 5
            
        # Content matches (lowest priority)
        if content.content_html and query_lower in content.content_html.lower():
            score += 2
        if content.content_html_en and query_lower in content.content_html_en.lower():
            score += 2
            
        return score
    
    # Sort by relevance score (highest first), then by created_at
    sorted_results = sorted(results, key=lambda x: (calculate_relevance(x), x.created_at), reverse=True)
    
    return sorted_results

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

def get_content_in_language(db: Session, content_id: int, target_language: Language) -> Optional[Content]:
    """Get content in a different language by reference_id"""
    # First get the current content
    current_content = db.query(Content).filter(Content.id == content_id).first()
    if not current_content:
        return None
    
    # If already in target language, return the same content
    if current_content.language == target_language:
        return current_content
    
    # If no reference_id, check if the content has bilingual fields
    if not current_content.reference_id:
        # Check if this content has the alternative language fields populated
        if target_language == Language.ENGLISH:
            if current_content.title_en and current_content.content_html_en:
                return current_content  # Will be handled by frontend to use _en fields
        return None
    
    # Find content with same reference_id but different language
    alternative_content = db.query(Content).filter(
        Content.reference_id == current_content.reference_id,
        Content.language == target_language
    ).first()
    
    return alternative_content

def check_language_availability(db: Session, content_id: int, target_language: Language) -> bool:
    """Check if content is available in target language"""
    current_content = db.query(Content).filter(Content.id == content_id).first()
    if not current_content:
        return False
    
    # If already in target language
    if current_content.language == target_language:
        return True
    
    # Check if bilingual fields exist
    if not current_content.reference_id:
        if target_language == Language.ENGLISH:
            return bool(current_content.title_en and current_content.content_html_en)
        return False
    
    # Check if alternative language content exists
    alternative_content = db.query(Content).filter(
        Content.reference_id == current_content.reference_id,
        Content.language == target_language
    ).first()
    
    return alternative_content is not None
