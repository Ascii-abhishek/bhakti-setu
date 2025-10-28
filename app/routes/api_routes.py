from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.models import ContentType
from app.schemas import ContentResponse

router = APIRouter(prefix="/api")


@router.get("/contents", response_model=List[ContentResponse])
def get_contents(
    content_type: Optional[ContentType] = None,
    shuffle: bool = Query(True),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all contents with optional filtering"""
    from app.services import content_service
    contents = content_service.get_all_contents(
        db, content_type=content_type,
        skip=skip, limit=limit, shuffle=shuffle
    )
    return contents


@router.get("/contents/{content_id}", response_model=ContentResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    """Get a specific content by ID"""
    from app.services import content_service
    from fastapi import HTTPException
    
    content = content_service.get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.get("/search", response_model=List[ContentResponse])
def search_contents(
    q: str,
    content_type: Optional[ContentType] = None,
    db: Session = Depends(get_db)
):
    """Search contents"""
    from app.services import content_service
    contents = content_service.search_contents(db, q, content_type)
    return contents


@router.get("/random", response_model=ContentResponse)
def get_random_content(
    content_type: Optional[ContentType] = None,
    db: Session = Depends(get_db)
):
    """Get a random content"""
    from app.services import content_service
    from fastapi import HTTPException
    
    content = content_service.get_random_content(db, content_type)
    if not content:
        raise HTTPException(status_code=404, detail="No content found")
    return content
