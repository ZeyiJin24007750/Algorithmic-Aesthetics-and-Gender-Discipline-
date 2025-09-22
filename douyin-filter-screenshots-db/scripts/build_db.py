#!/usr/bin/env python3
"""
Scan screenshots/, merge/update data/metadata.csv, and generate gallery.md.

- If a file exists in screenshots/ but not in CSV, a new row is appended with
  empty values (try to parse filter_name, whitening, face_slim from filename).
- Existing rows are preserved (do not overwrite user-edited fields).
- Output CSV is sorted by filter_name (then filename) for readability.
- Generates a simple Markdown gallery table with relative links.

Filename parsing:
  <name>[_-]wh<0-100>[_-]fs<0-100>.png|jpg
Examples:
  Retouch_wh30_fs20.png  -> name=Retouch, whitening=30, face_slim=20
  Nature.png             -> name=Nature, whitening=?, face_slim=?
"""

from pathlib import Path
import csv, re, datetime

ROOT = Path(__file__).resolve().parents[1]
SCREEN_DIR = ROOT / "screenshots"
DATA_DIR = ROOT / "data"
CSV_PATH = DATA_DIR / "metadata.csv"
GALLERY = ROOT / "gallery.md"

IMG_EXTS = {".png", ".jpg", ".jpeg"}

PAT = re.compile(
    r"""^(?P<name>.+?)
        (?:[_-]wh(?P<wh>\d{1,3}))?
        (?:[_-]fs(?P<fs>\d{1,3}))?
        \.(?:png|jpg|jpeg)$
    """,
    re.IGNORECASE | re.VERBOSE
)

def read_csv_rows():
    rows = []
    if CSV_PATH.exists():
        with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append({k: (v or "").strip() for k, v in r.items()})
    return rows

def write_csv_rows(rows):
    fieldnames = ["filename","filter_name","whitening_value","face_slim_ratio","source","captured_at","tags","notes"]
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})

def scan_images():
    if not SCREEN_DIR.exists():
        return []
    files = []
    for p in SCREEN_DIR.iterdir():
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            files.append(p.name)
    return sorted(files, key=str.lower)

def parse_from_filename(fname):
    m = PAT.match(fname)
    result = {"filter_name":"", "whitening_value":"", "face_slim_ratio":""}
    if m:
        name = m.group("name") or ""
        wh = m.group("wh") or ""
        fs = m.group("fs") or ""
        # clean name: replace separators with spaces
        name = re.sub(r"[-_]+", " ", name).strip()
        result["filter_name"] = name
        result["whitening_value"] = wh
        result["face_slim_ratio"] = fs
    return result

def merge(rows, images):
    # index by filename
    by_file = {r.get("filename",""): r for r in rows if r.get("filename")}
    changed = False
    today = datetime.date.today().isoformat()

    for img in images:
        if img not in by_file:
            # new row
            parsed = parse_from_filename(img)
            row = {
                "filename": img,
                "filter_name": parsed["filter_name"],
                "whitening_value": parsed["whitening_value"],
                "face_slim_ratio": parsed["face_slim_ratio"],
                "source": "Douyin",
                "captured_at": today,
                "tags": "",
                "notes": "",
            }
            rows.append(row)
            changed = True

    # remove rows for files that no longer exist
    existing = set(images)
    rows = [r for r in rows if r.get("filename") in existing]

    # sort
    rows.sort(key=lambda r: (r.get("filter_name","").lower(), r.get("filename","").lower()))
    return rows, changed

def generate_gallery(rows):
    lines = []
    lines.append("# Gallery\n")
    lines.append("| Image | Filter | Whiten | Face Slim | Notes |")
    lines.append("|---|---|---:|---:|---|")
    for r in rows:
        img_rel = f"screenshots/{r.get('filename','')}"
        filt = r.get("filter_name","")
        wh = r.get("whitening_value","")
        fs = r.get("face_slim_ratio","")
        notes = r.get("notes","")
        lines.append(f"| ![]({img_rel}) | {filt} | {wh} | {fs} | {notes} |")
    GALLERY.write_text("\\n".join(lines), encoding="utf-8")

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv_rows()
    images = scan_images()
    rows, _ = merge(rows, images)
    write_csv_rows(rows)
    generate_gallery(rows)
    print(f"Updated {CSV_PATH} with {len(rows)} rows.")
    print(f"Wrote {GALLERY}")

if __name__ == "__main__":
    main()
