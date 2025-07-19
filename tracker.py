import csv
import os

TRACKER_FILE = "article_tracker.csv"
PLATFORMS = ["twitter", "linkedin"]  # Add more if needed

def init_tracker(article_urls, tracker_file=TRACKER_FILE):
    """Ensure tracker CSV exists with all URLs. Adds new URLs if needed."""
    rows = []
    existing = {}
    if os.path.exists(tracker_file):
        with open(tracker_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing[row["url"]] = row

    # Build fieldnames
    fieldnames = ["url"]
    for platform in PLATFORMS:
        fieldnames += [
            f"{platform}_post",         # filename for generated post
            f"{platform}_approved",     # TRUE/FALSE/blank
            f"{platform}_uploaded"
        ]

    # Ensure all URLs are included
    for url in article_urls:
        url = url.strip()
        if not url:
            continue
        if url not in existing:
            row = {"url": url}
            for platform in PLATFORMS:
                row[f"{platform}_post"] = ""
                row[f"{platform}_approved"] = ""
                row[f"{platform}_uploaded"] = ""
            existing[url] = row
    rows = list(existing.values())

    # Write back the tracker
    with open(tracker_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def get_next_article_to_post(platform, tracker_file=TRACKER_FILE):
    """Returns the next (latest) article dict that doesn't have a post generated for the platform, or None."""
    with open(tracker_file, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    # Go from last to first (bottom-up)
    for row in reversed(reader):
        if not row[f"{platform}_post"]:
            return row
    return None

def mark_post_generated(url, platform, filename, tracker_file=TRACKER_FILE):
    """Update tracker file with the post filename for the given URL/platform."""
    with open(tracker_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row["url"] == url:
            row[f"{platform}_post"] = filename
    with open(tracker_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def set_post_approval(url, platform, approved, tracker_file=TRACKER_FILE):
    """Set approval flag for a platform's post on a given URL."""
    with open(tracker_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row["url"] == url:
            row[f"{platform}_approved"] = "TRUE" if approved else "FALSE"
    with open(tracker_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def get_post_filename(url, platform, tracker_file=TRACKER_FILE):
    with open(tracker_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row["url"] == url:
            return row[f"{platform}_post"]
    return None

def get_latest_incomplete_row(platforms, tracker_file=TRACKER_FILE):
    """Return the latest row (from the bottom) where any of the platforms are missing, and which platforms are missing."""
    with open(tracker_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in reversed(rows):
        missing = [platform for platform in platforms if not row[f"{platform}_post"]]
        if missing:
            return row, missing
    return None, []

def mark_post_uploaded(url, platform, tracker_file=TRACKER_FILE):
    """Set the upload flag for a given URL/platform."""
    with open(tracker_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row["url"] == url:
            row[f"{platform}_uploaded"] = "TRUE"
    with open(tracker_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        

def clear_post(url, platform, tracker_file=TRACKER_FILE):
    """Clears the post filename and approval flag for the given URL/platform."""
    with open(tracker_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if row["url"] == url:
            row[f"{platform}_post"] = ""
            row[f"{platform}_approved"] = ""
    with open(tracker_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
