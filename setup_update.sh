#!/bin/bash

# Bhakti Setu - Quick Setup Script
# This script helps you migrate to the new bilingual version

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Bhakti Setu - Bilingual Update Migration          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}→ Activating virtual environment...${NC}"
source venv/bin/activate

# Install/upgrade dependencies
echo -e "${YELLOW}→ Installing dependencies...${NC}"
pip install -r requirements.txt --quiet

# Run database migration
echo ""
echo -e "${YELLOW}→ Running database migration...${NC}"
python migrate_db.py

# Check if migration was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           Migration Completed Successfully! ✓             ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Start the server: uvicorn app.main:app --reload"
    echo "2. Visit http://localhost:8000 to see the new interface"
    echo "3. Check UPDATE_NOTES.md for detailed documentation"
    echo ""
    echo "New features available:"
    echo "  ✓ Bilingual content support (Hindi/English)"
    echo "  ✓ Apple-style glassmorphism UI"
    echo "  ✓ Language switcher in navbar"
    echo "  ✓ Tags system for content"
    echo "  ✓ Modern navigation with circular buttons"
    echo ""
else
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║              Migration Failed - See Errors Above           ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check database connection in app/config.py"
    echo "2. Ensure PostgreSQL is running"
    echo "3. Verify database credentials"
    echo "4. Check migrate_db.py for specific errors"
    exit 1
fi
