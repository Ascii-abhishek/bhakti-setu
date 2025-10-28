from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


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
