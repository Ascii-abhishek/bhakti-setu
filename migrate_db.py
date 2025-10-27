"""
Database migration script to add new fields to the contents table.
Run this script to update your existing database schema.
"""
from sqlalchemy import text
from app.database import engine

def migrate_database():
    """Add new columns to the contents table"""
    
    migrations = [
        # Add reference_id column
        "ALTER TABLE contents ADD COLUMN IF NOT EXISTS reference_id VARCHAR(100)",
        "CREATE INDEX IF NOT EXISTS idx_contents_reference_id ON contents(reference_id)",
        
        # Add English variant columns
        "ALTER TABLE contents ADD COLUMN IF NOT EXISTS title_en VARCHAR(255)",
        "CREATE INDEX IF NOT EXISTS idx_contents_title_en ON contents(title_en)",
        "ALTER TABLE contents ADD COLUMN IF NOT EXISTS summary_en TEXT",
        "ALTER TABLE contents ADD COLUMN IF NOT EXISTS content_html_en TEXT",
        
        # Add banner_url column
        "ALTER TABLE contents ADD COLUMN IF NOT EXISTS banner_url VARCHAR(500)",
        
        # Add tags column
        "ALTER TABLE contents ADD COLUMN IF NOT EXISTS tags VARCHAR(500)",
    ]
    
    with engine.connect() as conn:
        for migration in migrations:
            try:
                conn.execute(text(migration))
                conn.commit()
                print(f"✓ Executed: {migration[:60]}...")
            except Exception as e:
                print(f"✗ Error executing migration: {e}")
                print(f"  SQL: {migration}")
    
    print("\n✓ Database migration completed successfully!")
    print("\nNote: The following fields are now available:")
    print("  - reference_id: Links same content in different languages")
    print("  - title_en: English title (optional)")
    print("  - summary_en: English summary (optional)")
    print("  - content_html_en: English content (optional)")
    print("  - banner_url: Banner image URL for content page")
    print("  - tags: Comma-separated tags")

if __name__ == "__main__":
    print("Starting database migration...")
    print("=" * 60)
    migrate_database()
