# Bhakti Setu - Bilingual Content Update

## Summary of Changes

This update adds comprehensive bilingual support (Hindi/English) and modernizes the UI with Apple-style glassmorphism design.

## Key Features Added

### 1. **Bilingual Content Support**
- Content can now be stored in both Hindi and English
- Each content piece can have:
  - `title` and `title_en` (English title - optional)
  - `summary` and `summary_en` (English summary - optional)
  - `content_html` and `content_html_en` (English content - optional)
  - `reference_id` to link same content in different languages

### 2. **Tags System**
- Added `tags` field for comma-separated tags
- Tags are displayed at the bottom of content pages
- Helps categorize and organize content

### 3. **Language Switching**

#### Home Page (Global Language Switch)
- Language toggle icon in the top-right navbar
- Switches all content on the home page to selected language
- Language preference is stored in browser localStorage
- Reloads content tiles in the selected language

#### Content Page (Story-Level Language Switch)
- Language toggle switches only the current story/content
- Checks if content is available in target language
- Shows "Language Not Available" popup if content doesn't exist in requested language
- Seamlessly switches between Hindi and English versions

### 4. **Modern UI Updates**

#### Glassmorphism Design
- Apple-style glass navbar with blur effect
- Semi-transparent backgrounds with backdrop filters
- Modern, clean aesthetic matching latest macOS/iOS design

#### Updated Layouts

**Home Page:**
- Search bar moved to top navbar
- Glass effect navigation bar
- Language and theme switchers on the right
- No language badge on content tiles (cleaner look)
- Only content type badge shown

**Content Page:**
- Bhakti Setu logo on top-left
- Theme and language switcher icons on top-right
- Large round navigation arrows on left and right sides
- No home icon (use back arrow or logo to go home)
- Content meta information at bottom:
  - Tags on the left
  - Created date on the right (small font)

### 5. **Navigation Improvements**
- Left arrow: Go back to previous page
- Right arrow: Load next random content
- Removed home icon from content pages
- Logo in navbar always links to home

## Database Schema Updates

New columns added to `contents` table:
```sql
- reference_id (VARCHAR(100)) - Links content in different languages
- title_en (VARCHAR(255)) - English title (optional)
- summary_en (TEXT) - English summary (optional)
- content_html_en (TEXT) - English content (optional)
- tags (VARCHAR(500)) - Comma-separated tags
```

## Installation & Migration

### Step 1: Backup Your Database
```bash
# Create a backup of your current database
pg_dump your_database_name > backup_before_update.sql
```

### Step 2: Run Migration Script
```bash
# Run the migration to add new columns
python migrate_db.py
```

### Step 3: Restart the Application
```bash
# Restart your FastAPI server
uvicorn app.main:app --reload
```

## How to Use

### Adding Bilingual Content

1. **For Single Language Content:**
   - Fill in the regular fields (title, summary, content_html)
   - Leave English fields empty
   - Content will work in both Hindi/English modes (showing same content)

2. **For Bilingual Content (Same Document):**
   - Fill in Hindi fields: title, summary, content_html
   - Fill in English fields: title_en, summary_en, content_html_en
   - Set primary language (hindi or english)
   - Leave reference_id empty
   - Content will show appropriate language based on user selection

3. **For Separate Language Documents:**
   - Create Hindi version with a unique reference_id (e.g., "story-001")
   - Create English version with the same reference_id
   - Both documents will be linked
   - Language switcher will switch between documents

### Adding Tags
- Enter comma-separated tags in the tags field
- Example: `devotion, Krishna, bhakti, spiritual`
- Tags will appear at the bottom of content pages

## Language Switching Behavior

### Home Page
- Switching language affects the entire website
- All content tiles reload in selected language
- Preference is saved in browser

### Content Page
- Switching language affects only the current story
- If bilingual fields exist (title_en, etc.), shows those fields
- If reference_id exists, loads the linked document in target language
- If neither exists, shows "Language Not Available" popup

## API Endpoints Added

```
GET /api/contents/{content_id}/language/{target_language}
- Get content in specified language

GET /api/contents/{content_id}/check-language/{target_language}
- Check if content is available in target language
```

## Files Modified

### Backend
- `app/models/content.py` - Added new database columns
- `app/schemas.py` - Updated Pydantic schemas
- `app/services/content_service.py` - Added language switching logic
- `app/routes/story_routes.py` - Added new API endpoints

### Frontend
- `templates/index.html` - New layout with glass navbar
- `templates/content.html` - Updated content page layout
- `templates/admin.html` - Added new fields to admin form
- `static/css/styles.css` - Glassmorphism and modern styling
- `static/js/main.js` - Global language switching
- `static/js/content.js` - Story-level language switching
- `static/js/admin.js` - Handle new form fields

### New Files
- `migrate_db.py` - Database migration script
- `UPDATE_NOTES.md` - This file

## Design Philosophy

1. **Progressive Enhancement**: Existing content works without changes
2. **Optional Bilingual**: English fields are optional
3. **User Choice**: Users can switch language at any time
4. **Graceful Degradation**: Shows popup if language not available
5. **Modern UI**: Apple-inspired glassmorphism design
6. **Clean Interface**: Removed unnecessary badges and clutter

## Browser Compatibility

The glassmorphism effects require modern browsers with backdrop-filter support:
- Chrome 76+
- Safari 9+
- Firefox 103+
- Edge 79+

Fallback styles ensure usability on older browsers.

## Notes

- Language preference is stored in localStorage
- Theme preference is stored separately
- Reference ID should be unique across related content
- Tags are free-form text, comma-separated
- All English fields are optional

## Troubleshooting

**Language not switching?**
- Clear browser localStorage
- Check browser console for errors
- Verify API endpoints are responding

**Content not showing in English?**
- Ensure English fields are populated in database
- Check if content has reference_id linking to English version
- Verify target language is being passed correctly

**Glass effect not working?**
- Check browser compatibility
- Ensure CSS is loading correctly
- Verify backdrop-filter support in browser

## Future Enhancements

Potential improvements:
- Auto-translate feature
- More languages (Sanskrit, Tamil, etc.)
- Tag-based filtering
- Search by tags
- Language statistics in admin panel
