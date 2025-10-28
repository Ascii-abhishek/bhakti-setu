from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import timedelta
import uuid
from pathlib import Path

from app.database import get_db
from app.schemas import ContentResponse, ContentCreate, LoginRequest, Token
from app.services import content_service, auth_service
from app.utils.auth import create_access_token, verify_token
from app.config import settings

router = APIRouter(prefix="/api/admin")

# Upload directory
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


@router.post("/login", response_model=Token)
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


@router.post("/upload-image")
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


@router.post("/contents", response_model=ContentResponse)
def create_content(
    content: ContentCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(verify_token)
):
    """Create a new content (admin only)"""
    new_content = content_service.create_content(db, content.dict())
    return new_content


@router.delete("/contents/{content_id}")
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
