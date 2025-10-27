from app.config import settings
from typing import Optional

def authenticate_admin(username: str, password: str) -> bool:
    """Authenticate an admin using environment variables"""
    if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
        return True
    return False
