# Bhakti Setu - Quick Reference Guide

## 🎨 Visual Changes

### Home Page - Before vs After

**BEFORE:**
```
┌─────────────────────────────────────────┐
│ Bhakti Setu               [Theme Icon]  │ ← Gradient navbar
└─────────────────────────────────────────┘

         ┌─────────────────┐
         │   Search Bar    │  ← Separate section
         └─────────────────┘

┌───────┐ ┌───────┐ ┌───────┐
│ Image │ │ Image │ │ Image │
│ Title │ │ Title │ │ Title │
│ Text  │ │ Text  │ │ Text  │
│[Story]│ │[Story]│ │[Story]│
│[Hindi]│ │[Eng]  │ │[Hindi]│ ← Language badge
└───────┘ └───────┘ └───────┘
```

**AFTER:**
```
┌──────────────────────────────────────────────────────┐
│ Bhakti Setu  [Search Bar]  [🌐][☀️]                │ ← Glass navbar
└──────────────────────────────────────────────────────┘
                                    ↑        ↑
                           Language Theme
                           Toggle  Toggle

┌───────┐ ┌───────┐ ┌───────┐
│ Image │ │ Image │ │ Image │
│ Title │ │ Title │ │ Title │
│ Text  │ │ Text  │ │ Text  │
│[Story]│ │[Story]│ │[Story]│ ← Only content type
└───────┘ └───────┘ └───────┘
```

### Content Page - Before vs After

**BEFORE:**
```
┌──────────────────┐
│ [🏠] [←]        │ ← Left sidebar
└──────────────────┘
                         ┌──────────────┐
         Content         │     [→]      │ ← Right sidebar
         Area            └──────────────┘
```

**AFTER:**
```
┌─────────────────────────────────────────────┐
│ Bhakti Setu                      [🌐][☀️]  │ ← Glass navbar
└─────────────────────────────────────────────┘

    (←)                                  (→)
     ↑                                    ↑
  Previous         Content            Next
   Button           Area             Button

           [Tags]              [Date] ← Bottom meta
           ─────────────────────────
```

## 🌐 Language Switching Behavior

### Scenario 1: Home Page Language Switch
```
User clicks [🌐] → Toggle Hindi ⟷ English
                 ↓
         Reload all cards in selected language
                 ↓
         Store preference in browser
```

### Scenario 2: Content Page Language Switch (Bilingual Fields)
```
Hindi content with English fields filled:
┌─────────────────────────────────┐
│ title: "राम कथा"                │
│ title_en: "Story of Ram"        │
│ summary: "..."                  │
│ summary_en: "..."               │
│ content_html: "..."             │
│ content_html_en: "..."          │
└─────────────────────────────────┘

User clicks [🌐] → Show English fields
User clicks [🌐] → Show Hindi fields
```

### Scenario 3: Content Page Language Switch (Linked Documents)
```
Hindi Document (reference_id: "ram-001")
┌─────────────────────────────────┐
│ id: 1                           │
│ language: hindi                 │
│ title: "राम कथा"                │
│ reference_id: "ram-001"         │
└─────────────────────────────────┘

English Document (reference_id: "ram-001")
┌─────────────────────────────────┐
│ id: 2                           │
│ language: english               │
│ title: "Story of Ram"           │
│ reference_id: "ram-001"         │
└─────────────────────────────────┘

User clicks [🌐] → Load document id: 2
User clicks [🌐] → Load document id: 1
```

### Scenario 4: Language Not Available
```
User on Hindi content
User clicks [🌐] to switch to English
         ↓
   No English version exists
         ↓
┌─────────────────────────────────┐
│ ⚠ Language Not Available        │
│                                 │
│ This content is not available   │
│ in the selected language.       │
│                                 │
│         [Close]                 │
└─────────────────────────────────┘
```

## 📝 Admin Panel - New Fields

```
Content Form:
├─ Content Type ────────┐
├─ Language ────────────┤
├─ Title ───────────────┤
├─ Title (English) ─────┤ ← NEW
├─ Header ──────────────┤
├─ Summary ─────────────┤
├─ Summary (English) ───┤ ← NEW
├─ Poster URL ──────────┤
├─ Content HTML ────────┤
├─ Content HTML (EN) ───┤ ← NEW
├─ Tags ────────────────┤ ← NEW (comma-separated)
├─ Reference ID ────────┤ ← NEW (link languages)
└─ Audio URL ───────────┘
```

## 🔧 Database Schema

```sql
-- New Columns Added
ALTER TABLE contents ADD COLUMN reference_id VARCHAR(100);
ALTER TABLE contents ADD COLUMN title_en VARCHAR(255);
ALTER TABLE contents ADD COLUMN summary_en TEXT;
ALTER TABLE contents ADD COLUMN content_html_en TEXT;
ALTER TABLE contents ADD COLUMN tags VARCHAR(500);

-- Indexes Created
CREATE INDEX idx_contents_reference_id ON contents(reference_id);
CREATE INDEX idx_contents_title_en ON contents(title_en);
```

## 🎯 Use Cases

### Use Case 1: Bilingual Story in Same Document
**Best for:** Content where both languages should be maintained together

```
Step 1: Create content with language = hindi
Step 2: Fill Hindi fields (title, summary, content_html)
Step 3: Fill English fields (title_en, summary_en, content_html_en)
Step 4: Leave reference_id empty
Step 5: Add tags: "story, devotion, bilingual"

Result: One document showing appropriate language based on user selection
```

### Use Case 2: Separate Language Documents
**Best for:** Content translated/adapted separately

```
Step 1: Create Hindi version
  - language = hindi
  - title = "राम कथा"
  - reference_id = "ram-story-001"
  
Step 2: Create English version
  - language = english
  - title = "Story of Ram"
  - reference_id = "ram-story-001"  ← Same reference_id

Result: Two documents linked by reference_id, switcher loads correct document
```

### Use Case 3: Hindi-Only Content
**Best for:** Content not available in English yet

```
Step 1: Create content with language = hindi
Step 2: Fill Hindi fields only
Step 3: Leave all English fields empty
Step 4: Leave reference_id empty

Result: Shows in both modes, but displays Hindi content
        English switch shows "Language Not Available"
```

## 🎨 CSS Classes Reference

```css
/* Glass Effect */
.glass-navbar {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px) saturate(180%);
}

/* Navigation Buttons */
.btn-nav-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  /* Glass effect + hover animations */
}

/* Tag Badges */
.tag-badge {
  backdrop-filter: blur(10px);
  border-radius: 15px;
}

/* Content Meta Info */
.content-meta {
  border-top: 2px solid var(--border-color);
  /* Flexbox layout for tags and date */
}
```

## 🚀 Quick Start Commands

```bash
# 1. Run migration
python migrate_db.py

# 2. Start server
uvicorn app.main:app --reload

# 3. Or use the setup script
./setup_update.sh

# 4. Access application
open http://localhost:8000
```

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Glass effect not visible | Check browser supports backdrop-filter |
| Language not switching | Clear localStorage, check console |
| Admin form not saving new fields | Verify schemas.py updated correctly |
| Migration fails | Check database connection, run manually |
| Tags not showing | Ensure content.tags has comma-separated values |

## 📱 Responsive Behavior

**Desktop (> 768px):**
- Full glass navbar with search
- Side navigation arrows visible
- All features enabled

**Mobile (< 768px):**
- Search bar hidden in navbar (can be added to separate section)
- Smaller navigation arrows
- Stacked content meta (tags above date)
- Touch-friendly button sizes
