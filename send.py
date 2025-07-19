import os
import csv
import tweepy
import re
from tracker import mark_post_uploaded  # you must have this function
from config import load_config
cfg = load_config()

# --- Twitter credentials ---
TWITTER_API_KEY = cfg.get("TWITTER_API_KEY")
TWITTER_API_SECRET = cfg.get("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = cfg.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = cfg.get("TWITTER_ACCESS_SECRET")

TRACKER_FILE = "article_tracker.csv"
LOCAL_ROOT = "post_outputs"
PLATFORM = "twitter"
TWEET_CHAR_LIMIT = 280
TCO_URL_LENGTH = 23

def tweet_length_with_urls(text):
    # Regex for URLs: (http or https, followed by non-space chars)
    url_regex = r"https?://\S+"
    urls = re.findall(url_regex, text)
    # Remove URLs from text length, add 23 per URL
    len_without_urls = len(re.sub(url_regex, '', text))
    return len_without_urls + len(urls) * TCO_URL_LENGTH

def post_tweet(text: str):
    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_SECRET
    )
    response = client.create_tweet(text=text)
    tweet_id = response.data.get("id")
    print(f"✅ Tweet posted! https://x.com/i/web/status/{tweet_id}")
    return tweet_id

def main():
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    for row in reversed(rows):  # Start from bottom
        approved = row.get(f"{PLATFORM}_approved", "").strip().upper() == "TRUE"
        uploaded = row.get(f"{PLATFORM}_uploaded", "").strip().upper() == "TRUE"
        post_file = row.get(f"{PLATFORM}_post", "").strip()
        url = row.get("url", "")

        if approved and not uploaded and post_file:
            file_path = os.path.join(LOCAL_ROOT, post_file)
            if not os.path.exists(file_path):
                print(f"⚠️ Skipping: file not found: {file_path}")
                continue

            with open(file_path, encoding="utf-8") as pf:
                tweet_text = pf.read().strip()

            # Check tweet length including URL handling
            tweet_len = tweet_length_with_urls(tweet_text)
            if tweet_len > TWEET_CHAR_LIMIT:
                print(f"❌ Tweet too long ({tweet_len} chars, limit {TWEET_CHAR_LIMIT}). Skipping.")
                continue

            print(f"\nAbout to send tweet for: {url}\n---\n{tweet_text}\n---")
            try:
                tweet_id = post_tweet(tweet_text)
                mark_post_uploaded(url, PLATFORM, tracker_file=TRACKER_FILE)
                print("Marked as uploaded in tracker.")
            except Exception as e:
                print(f"❌ Failed to post: {e}")
            break  # Only one post per run

    else:
        print("No approved, pending tweets found.")

if __name__ == "__main__":
    main()
