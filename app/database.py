from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import settings
from app.models import Base

# SQLAlchemy database engine with SSL support for Neon
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    # connect_args={"sslmode": "require", "channel_binding": "require"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
