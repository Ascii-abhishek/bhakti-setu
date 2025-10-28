from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routes import public_routes, api_routes, admin_routes
from app.database import init_db
from app.config import settings

# Initialize database
init_db()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(public_routes.router)
app.include_router(api_routes.router)
app.include_router(admin_routes.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
