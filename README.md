AI-Powered Social Media & RSS Workflow

This project automates the process of scraping articles from florisera.com, generating AI-powered social media posts, and managing an approval workflow before publishing to Twitter and LinkedIn.
Features

    Scrapes new article URLs from the florisera.com sitemap

    Extracts and summarizes article content using BeautifulSoup and GPT

    Generates social media post drafts (Twitter and LinkedIn)

    Manual approval workflow for all generated posts

    Automated posting to Twitter via API

    Tracks post status for each article and platform

    Includes both CLI and PyQt5-based GUI

Project Structure

Approve.py           # CLI for approving/denying posts
crawler.py           # Fetches article URLs from sitemap
main.py              # Extracts data and generates post drafts
send.py              # Posts approved tweets to Twitter
tracker.py           # CSV tracker for posts and statuses
socialmedia.py       # Social media prompt templates
webparsing.py        # Utilities for extracting and formatting article data
config.py            # Loads config from file (API keys, etc.)
GUI.py               # PyQt5 GUI for the workflow
article_tracker.csv  # Tracks articles and post statuses
post_outputs/        # Generated post drafts for each platform
bin/                 # Denied post drafts (optional)

Usage

    Install dependencies:

pip install requests beautifulsoup4 tweepy PyQt5

Add a config.txt file with your API keys and settings:

    API_URL=your_openai_endpoint
    API_KEY=your_openai_key
    TWITTER_API_KEY=your_twitter_key
    TWITTER_API_SECRET=your_twitter_secret
    TWITTER_ACCESS_TOKEN=your_twitter_access_token
    TWITTER_ACCESS_SECRET=your_twitter_access_secret

    Run the workflow:

        Crawl articles:
        python crawler.py

        Generate social media drafts:
        python main.py 5
        (replace 5 with the number of articles to process)

        Approve or deny posts:
        python Approve.py

        Post to Twitter:
        python send.py

        (Optional GUI: python GUI.py)

Notes

    Keep your config.txt and any API keys out of version control (.gitignore).

    You can add support for more platforms by extending socialmedia.py and related scripts.
