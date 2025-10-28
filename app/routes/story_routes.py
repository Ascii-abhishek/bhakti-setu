from fastapi import APIRouter, Request, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import timedelta
import os
import uuid
from pathlib import Path

from app.database import get_db
from app.models import ContentType, Language
from app.schemas import ContentResponse, ContentCreate, LoginRequest, Token
from app.services import content_service, auth_service
from app.utils.auth import create_access_token, verify_token
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Upload directory
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Public routes


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Render home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/content/{content_id}", response_class=HTMLResponse)
def view_content(request: Request, content_id: int):
    """Render content view page"""
    return templates.TemplateResponse("content.html", {"request": request, "content_id": content_id})


@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    """Render admin page"""
    return templates.TemplateResponse("admin.html", {"request": request})

# API routes


@router.get("/api/contents", response_model=List[ContentResponse])
def get_contents(
    content_type: Optional[ContentType] = None,
    language: Optional[Language] = None,
    shuffle: bool = Query(True),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all contents with optional filtering"""
    contents = content_service.get_all_contents(
        db, content_type=content_type, language=language,
        skip=skip, limit=limit, shuffle=shuffle
    )
    return contents


@router.get("/api/contents/{content_id}", response_model=ContentResponse)
def get_content(content_id: int, db: Session = Depends(get_db)):
    """Get a specific content by ID"""
    content = content_service.get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.get("/api/search", response_model=List[ContentResponse])
def search_contents(
    q: str,
    content_type: Optional[ContentType] = None,
    language: Optional[Language] = None,
    db: Session = Depends(get_db)
):
    """Search contents"""
    contents = content_service.search_contents(db, q, content_type, language)
    return contents


@router.get("/api/random", response_model=ContentResponse)
def get_random_content(
    content_type: Optional[ContentType] = None,
    db: Session = Depends(get_db)
):
    """Get a random content"""
    content = content_service.get_random_content(db, content_type)
    if not content:
        raise HTTPException(status_code=404, detail="No content found")
    return content


@router.get("/api/contents/{content_id}/language/{target_language}", response_model=ContentResponse)
def get_content_in_language(
    content_id: int,
    target_language: Language,
    db: Session = Depends(get_db)
):
    """Get content in specified language"""
    content = content_service.get_content_in_language(db, content_id, target_language)
    if not content:
        raise HTTPException(status_code=404, detail="Content not available in this language")
    return content


@router.get("/api/contents/{content_id}/check-language/{target_language}")
def check_language_availability(
    content_id: int,
    target_language: Language,
    db: Session = Depends(get_db)
):
    """Check if content is available in target language"""
    is_available = content_service.check_language_availability(db, content_id, target_language)
    return {"available": is_available}

# Admin routes


@router.post("/api/admin/login", response_model=Token)
def login(login_request: LoginRequest):
    """Admin login"""
    is_authenticated = auth_service.authenticate_admin(login_request.username, login_request.password)
    if not is_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": login_request.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/admin/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    current_admin=Depends(verify_token)
):
    """Upload an image file (admin only)"""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Return URL path
        image_url = f"/static/uploads/{unique_filename}"
        return {"url": image_url, "filename": unique_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.post("/api/admin/contents", response_model=ContentResponse)
def create_content(
    content: ContentCreate,
    db: Session = Depends(get_db)
):
    """Create a new content (admin only)"""
    new_content = content_service.create_content(db, content.dict())
    return new_content


@router.delete("/api/admin/contents/{content_id}")
def delete_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(verify_token)
):
    """Delete a content (admin only)"""
    success = content_service.delete_content(db, content_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"message": "Content deleted successfully"}
