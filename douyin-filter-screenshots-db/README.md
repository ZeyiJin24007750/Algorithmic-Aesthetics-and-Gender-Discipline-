# Douyin Filter Screenshots DB

A structured repo for **Douyin (抖音) filter** screenshots with a simple metadata database (CSV) and auto-generated gallery.

## Folder structure

```
douyin-filter-screenshots-db/
├─ screenshots/           # Put all your .png/.jpg here (exported from phone/computer)
├─ data/
│  └─ metadata.csv        # Filter name + default params (whitening/face-slim) + notes
├─ scripts/
│  └─ build_db.py         # Scans screenshots, updates CSV, generates a gallery
├─ gallery.md             # Auto-generated thumbnail-less gallery table (relative links)
└─ .gitattributes, .gitignore
```

## How to use

1. **Drop images** into `screenshots/`.  
   - Recommended filename format to auto-parse:  
     `FILTERNAME_wh30_fs20.png` (wh = whitening value, fs = face-slim ratio).  
     Examples: `Retouch_wh30_fs20.png`, `Nature.png`.

2. **Update or create metadata**:
   - Option A: Edit `data/metadata.csv` manually in Excel/Numbers.
   - Option B: Run the script to scaffold a CSV row for every image (keeps your edits):
     ```bash
     python3 scripts/build_db.py
     ```

3. **Generate gallery**:
   - The script also writes `gallery.md` (a Markdown table) each time you run it.

4. **Commit & push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initialize Douyin filter screenshots DB"
   git branch -M main
   git remote add origin https://github.com/yourname/douyin-filter-screenshots-db.git
   git push -u origin main
   ```

## CSV schema

| column            | meaning                                      |
|-------------------|----------------------------------------------|
| filename          | The image file name in `screenshots/`        |
| filter_name       | Filter name (e.g., Retouch, Nature…)         |
| whitening_value   | Default whitening value (0-100 or app scale) |
| face_slim_ratio   | Default face-slim ratio (0-100 or app scale) |
| source            | Where the screenshot came from (e.g., Douyin)|
| captured_at       | When captured (YYYY-MM-DD)                   |
| tags              | Semicolon-separated tags                     |
| notes             | Free-form notes                              |

> ⚠️ **If you have many large images**, consider enabling **Git LFS** for `.png`/`.jpg` files.

## Legal / Fair use note

These screenshots are captured for documentation/research purposes. Ensure that sharing them complies with Douyin's terms and local laws. Avoid uploading personal or sensitive information in screenshots.

