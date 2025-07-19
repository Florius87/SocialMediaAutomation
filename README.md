# AI-Powered Social Media

This project automates the process of scraping articles from [florisera.com](https://florisera.com), generating AI-powered social media posts, and managing an approval workflow before publishing to Twitter and LinkedIn.

## Features

- Scrapes new article URLs from the florisera.com sitemap
- Extracts and summarizes article content using BeautifulSoup and GPT
- Generates social media post drafts (Twitter and LinkedIn)
- Manual approval workflow for all generated posts
- Automated posting to Twitter via API
- Tracks post status for each article and platform
- Includes both CLI and PyQt5-based GUI

## Project Structure

| File/Folder           | Purpose                                     |
|-----------------------|---------------------------------------------|
| Approve.py            | CLI for approving/denying posts             |
| crawler.py            | Fetches article URLs from sitemap           |
| main.py               | Extracts data and generates post drafts     |
| send.py               | Posts approved tweets to Twitter            |
| tracker.py            | CSV tracker for posts and statuses          |
| socialmedia.py        | Social media prompt templates               |
| webparsing.py         | Extracts and formats article data           |
| config.py             | Loads config (API keys, etc.)               |
| GUI.py                | PyQt5 GUI for the workflow                  |
| article_tracker.csv   | Tracks articles and post statuses           |
| post_outputs/         | Generated post drafts for each platform     |
| bin/                  | Denied post drafts (optional)               |


## Usage



1. **Install dependencies:**

    ```bash
    pip install requests beautifulsoup4 tweepy PyQt5
    ```

2. **Add a `config.txt` file with your API keys and settings:**

    ```
    API_URL=your_openai_endpoint
    API_KEY=your_openai_key
    TWITTER_API_KEY=your_twitter_key
    TWITTER_API_SECRET=your_twitter_secret
    TWITTER_ACCESS_TOKEN=your_twitter_access_token
    TWITTER_ACCESS_SECRET=your_twitter_access_secret
    ```

3. **Run the Workflow (Recommended: GUI):**

    Simply start the graphical workflow manager:

    ```bash
    python GUI.py
    ```

    The GUI will let you:
    - Crawl for new articles
    - Generate AI-powered social media posts
    - Approve or deny drafts
    - Publish approved posts to Twitter

4. **Manual (CLI) Usage (Advanced/Alternative):**

    If you prefer running steps individually via the command line, you can use:

    ```bash
    python crawler.py         # Crawl for new articles
    python main.py 5          # Generate posts for up to 5 articles
    python Approve.py         # Approve or deny generated posts
    python send.py            # Publish approved posts to Twitter
    ```

    *(Replace 5 with your preferred number of articles to process)*

## Usage
## Notes

- You can add support for more platforms by extending `socialmedia.py` and related scripts.

---
