# Bhakti Setu - Additional Updates

## Changes Summary

This document describes the additional enhancements made to the Bhakti Setu project.

## 1. Toast Notification for Language Unavailability

**Changed:** Language unavailability notification from modal to toast

**Before:**
- Modal popup in center of screen
- Required user to click "Close" button
- Blocked the entire interface

**After:**
- Toast notification slides in from top-right
- Auto-dismisses after 2 seconds
- Non-intrusive, doesn't block interface
- Can be manually dismissed with close button

**Files Modified:**
- `templates/content.html` - Replaced modal with toast component
- `static/js/content.js` - Updated to use Bootstrap Toast API
- `static/css/styles.css` - Added toast styling with glass effect

## 2. Banner Image Field

**Added:** Separate banner image for content page display

**Purpose:**
- **Poster**: Shows on content tiles (home page cards)
- **Banner**: Shows inside content detail page

This separation allows different image ratios and designs for different contexts.

**Database Schema:**
```sql
ALTER TABLE contents ADD COLUMN banner_url VARCHAR(500);
```

**Files Modified:**
- `app/models/content.py` - Added banner_url column
- `app/schemas.py` - Updated schemas with banner_url
- `static/js/content.js` - Use banner_url instead of poster_url in content page
- `migrate_db.py` - Added banner_url to migration script

## 3. Image Upload Functionality

**Changed:** URL input fields to file upload

### Why Image Upload?

**Pros:**
- ✓ Easier for admins (no need to host images elsewhere)
- ✓ All assets in one place
- ✓ No broken links from external sources
- ✓ Consistent performance
- ✓ Can apply image optimization later

**Cons:**
- ✗ Slightly larger database deployment size
- ✗ Images served from same server as app

**Recommendation:** Image upload is the right choice for your use case because:
1. Content is relatively small-scale (not millions of images)
2. Simplifies admin workflow significantly
3. FastAPI serves static files efficiently
4. Can easily migrate to CDN later if needed

### Implementation Details

**Storage Location:**
```
static/uploads/
  ├── {uuid}.jpg
  ├── {uuid}.png
  └── ...
```

**File Handling:**
- Unique filename: `UUID + original extension`
- Allowed formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Max file size: Default (can be configured)
- Path stored in database: `/static/uploads/{filename}`

**API Endpoint:**
```
POST /api/admin/upload-image
Authorization: Bearer {token}
Body: multipart/form-data with 'file' field

Response:
{
  "url": "/static/uploads/{uuid}.jpg",
  "filename": "{uuid}.jpg"
}
```

**Security:**
- Admin authentication required
- File extension validation
- Unique filename prevents conflicts
- Served as static files (no execution risk)

**Files Modified:**
- `app/routes/story_routes.py` - Added upload endpoint and file handling
- `templates/admin.html` - Changed URL inputs to file inputs
- `static/js/admin.js` - Added image upload handler with preview
- `static/uploads/` - Created directory for uploaded images

### Admin Form Changes

**Before:**
```html
<input type="url" id="posterUrl" placeholder="https://...">
```

**After:**
```html
<input type="file" id="posterImage" accept="image/*">
<div id="posterPreview"></div>
<!-- URL stored in hidden field after upload -->
```

**User Experience:**
1. Admin selects image file
2. Image uploads immediately
3. Preview shows with success indicator
4. URL automatically populated in hidden field
5. On form submit, URL is saved to database

## 4. Enhanced Search with Relevance Scoring

**Improved:** Search now includes tags and uses intelligent ranking

### Search Fields (in order of relevance):

| Field | Relevance Score | Description |
|-------|----------------|-------------|
| title, title_en | 10 | Highest priority - exact title matches |
| tags | 8 | Very relevant - categorization |
| summary, summary_en | 5 | Moderate - description matches |
| content_html, content_html_en | 2 | Lowest - full content matches |

### Search Algorithm:

```python
# Example: Searching for "Krishna"
1. Check title fields → Score: 10 if match
2. Check tags → Score: 8 if match
3. Check summary → Score: 5 if match
4. Check content → Score: 2 if match

Results sorted by:
- Total relevance score (descending)
- Created date (newest first for same score)
```

### Examples:

**Query:** "devotion"

**Results Order:**
1. Content with "devotion" in title (score: 10)
2. Content with "devotion" in tags (score: 8)
3. Content with "devotion" in summary (score: 5)
4. Content with "devotion" in text (score: 2)

**Query:** "Krishna bhakti"

**Results Order:**
1. Title: "Krishna Bhakti Story" (score: 10)
2. Tags: "Krishna, bhakti, devotion" (score: 8)
3. Summary mentioning "Krishna bhakti" (score: 5)
4. Content text with both words (score: 2)

### Benefits:

- ✓ Most relevant results first
- ✓ Tags make categorization searchable
- ✓ Bilingual search (searches both Hindi and English fields)
- ✓ No false negatives (all matching content found)
- ✓ Logical ranking that matches user expectations

**Files Modified:**
- `app/services/content_service.py` - Complete rewrite of search_contents function

## Migration Instructions

### Step 1: Run Database Migration

```bash
python migrate_db.py
```

This will add the `banner_url` column to your database.

### Step 2: Test Image Upload

1. Log into admin panel
2. Try uploading a poster image
3. Try uploading a banner image
4. Verify images show in preview
5. Submit form and check content display

### Step 3: Test Search Enhancement

1. Add tags to some content (e.g., "Krishna, devotion, bhakti")
2. Search for terms in title → Should rank highest
3. Search for tag names → Should rank high
4. Search for summary words → Should rank medium
5. Verify order makes sense

## Image Upload Best Practices

### For Optimal Performance:

1. **Image Dimensions:**
   - Poster (tiles): 400x300px or 800x600px
   - Banner (content): 1200x400px or 1600x600px

2. **File Size:**
   - Keep under 500KB per image
   - Use JPEG for photos
   - Use PNG for graphics with transparency
   - Use WebP for best compression (modern browsers)

3. **File Names:**
   - Don't worry about names - system generates unique IDs
   - System preserves original extension

### Future Optimization Options:

If image loading becomes slow in the future:

1. **Image Compression:**
   - Add PIL/Pillow to resize/compress on upload
   - Generate thumbnails automatically

2. **CDN Integration:**
   - Upload to Cloudinary, AWS S3, or similar
   - Minimal code changes needed

3. **Lazy Loading:**
   - Already implemented in browser for images
   - Can add progressive loading

4. **Caching:**
   - Add cache headers to static file serving
   - Browser will cache images automatically

## File Structure Updates

```
bhakti-setu/
├── static/
│   ├── uploads/          ← NEW: Uploaded images
│   │   ├── abc123.jpg
│   │   ├── def456.png
│   │   └── ...
│   ├── css/
│   ├── js/
│   └── ...
├── app/
│   ├── models/
│   │   └── content.py    ← Updated: banner_url field
│   ├── schemas.py        ← Updated: banner_url field
│   ├── routes/
│   │   └── story_routes.py ← Updated: upload endpoint
│   └── services/
│       └── content_service.py ← Updated: enhanced search
└── templates/
    ├── admin.html        ← Updated: file inputs
    └── content.html      ← Updated: toast notification
```

## API Changes

### New Endpoint:

```http
POST /api/admin/upload-image
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request:
  file: <binary image data>

Response:
{
  "url": "/static/uploads/uuid.jpg",
  "filename": "uuid.jpg"
}

Error Response:
{
  "detail": "File type not allowed. Allowed types: .jpg, .jpeg, .png, .gif, .webp"
}
```

### Updated Endpoint:

```http
GET /api/search?q={query}&language={lang}

Now searches:
- title, title_en
- tags (NEW)
- summary, summary_en
- content_html, content_html_en

Results ordered by relevance score
```

## Testing Checklist

- [ ] Toast notification appears from right
- [ ] Toast auto-dismisses after 2 seconds
- [ ] Poster upload works in admin
- [ ] Banner upload works in admin
- [ ] Image preview shows after upload
- [ ] Poster shows on tile (home page)
- [ ] Banner shows on content page
- [ ] Search includes tags
- [ ] Search results ordered by relevance
- [ ] Database migration successful
- [ ] No errors in console

## Troubleshooting

### Images not uploading?

- Check `static/uploads/` directory exists and is writable
- Verify auth token is valid
- Check file size (may need to increase FastAPI limits)
- Check file extension is in ALLOWED_EXTENSIONS

### Toast not showing?

- Ensure Bootstrap JS is loaded
- Check browser console for errors
- Verify `languageToast` element exists in HTML

### Search not working correctly?

- Verify tags are comma-separated
- Check database has tags populated
- Ensure SQLAlchemy case statement is supported

### Images loading slowly?

- Compress images before upload
- Consider resizing large images
- Check server resources
- Consider CDN for future scaling

## Performance Considerations

### Current Setup:
- Images served from FastAPI static files
- No caching configured (browser default)
- No image optimization

### Benchmarks:
- Small project: ✓ Perfect as-is
- Medium project (< 10GB images): ✓ Fine
- Large project (> 50GB images): Consider CDN

### When to Optimize:
- Wait until you have > 1000 images
- Wait until users report slow loading
- Premature optimization not needed

## Security Notes

- ✓ File extension validation prevents script uploads
- ✓ UUID filename prevents path traversal
- ✓ Admin authentication required
- ✓ Static file serving (no execution)
- ✓ No direct database access from upload

## Summary of Benefits

1. **Better UX**: Toast notifications are less intrusive
2. **Easier Admin**: Direct file upload vs hosting elsewhere
3. **Better Organization**: Poster vs Banner separation
4. **Smarter Search**: Relevance-based results
5. **Tag Support**: Better content categorization
6. **Bilingual Search**: Works across both languages

All changes are backward compatible - existing content works without modification!
