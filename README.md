# Hacker News Email Scraper

A small Python script that scrapes the top stories from Hacker News and sends them by email.

## What it does

- Fetches the Hacker News homepage
- Parses top story titles using BeautifulSoup
- Builds an HTML email message
- Sends the message via SMTP using environment variables

## Requirements

- Python 3.14+
- `beautifulsoup4`
- `requests`
- `python-dotenv`
- `ipykernel` (optional, for development/notebooks)

## Setup

1. Install dependencies:

```powershell
python -m pip install beautifulsoup4 requests python-dotenv
```

2. Create a `.env` file in the project root with the following values:

```env
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASS=your-email-password
TO_EMAIL=recipient@example.com
```

## Usage

Run the script with:

```powershell
python main.py
```

The script will send an email containing the current top Hacker News stories.

## Notes

- The script uses `news.ycombinator.com` to scrape story titles.
- Make sure your SMTP credentials are valid and that the SMTP host allows sign-in from this script.
