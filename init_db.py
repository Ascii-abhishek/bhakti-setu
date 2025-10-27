"""
Script to initialize the database
"""
from app.database import init_db
from app.config import settings

def initialize():
    """Initialize database tables"""
    print("Initializing database...")
    init_db()
    print("Database tables created successfully!")
    print(f"\nAdmin credentials are configured in .env file:")
    print(f"Username: {settings.ADMIN_USERNAME}")
    print(f"Password: {'*' * len(settings.ADMIN_PASSWORD)}")
    print("\n⚠️  IMPORTANT: Change the default password in production!")

if __name__ == "__main__":
    initialize()
