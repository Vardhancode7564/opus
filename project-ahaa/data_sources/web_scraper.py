"""Web Project Scraper - Scrapes project ideas from web pages."""

import requests
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)


def scrape_project_ideas(url):
    """
    Scrape a web page for project ideas.
    Attempts to extract project titles and descriptions from common HTML patterns.
    Returns a list of project dicts.
    """
    projects = []
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Strategy 1: Look for article/card patterns
        articles = soup.find_all(["article", "div"], class_=re.compile(
            r"(project|card|item|repo|listing)", re.IGNORECASE
        ))
        if articles:
            for article in articles[:50]:
                title_tag = article.find(["h1", "h2", "h3", "h4", "a"])
                desc_tag = article.find(["p", "span"])
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    desc = desc_tag.get_text(strip=True) if desc_tag else ""
                    link = ""
                    a_tag = article.find("a", href=True)
                    if a_tag:
                        link = a_tag["href"]
                        if link.startswith("/"):
                            from urllib.parse import urljoin
                            link = urljoin(url, link)

                    if title and len(title) > 3:
                        projects.append({
                            "project_title": title[:200],
                            "description": desc[:500],
                            "technologies": _extract_technologies(title + " " + desc),
                            "source": "web",
                            "project_link": link or url,
                        })

        # Strategy 2: If no articles found, look for heading + paragraph pairs
        if not projects:
            headings = soup.find_all(["h2", "h3", "h4"])
            for heading in headings[:30]:
                title = heading.get_text(strip=True)
                desc = ""
                next_elem = heading.find_next_sibling()
                if next_elem and next_elem.name == "p":
                    desc = next_elem.get_text(strip=True)

                if title and len(title) > 5:
                    projects.append({
                        "project_title": title[:200],
                        "description": desc[:500],
                        "technologies": _extract_technologies(title + " " + desc),
                        "source": "web",
                        "project_link": url,
                    })

    except requests.RequestException as e:
        logger.error(f"Error scraping {url}: {e}")
    except Exception as e:
        logger.error(f"Parsing error for {url}: {e}")

    return projects


def _extract_technologies(text):
    """Extract technology keywords from text."""
    tech_keywords = [
        "python", "java", "javascript", "react", "angular", "vue",
        "node", "django", "flask", "spring", "tensorflow", "pytorch",
        "machine learning", "deep learning", "nlp", "computer vision",
        "blockchain", "iot", "arduino", "raspberry pi", "android",
        "ios", "swift", "kotlin", "c++", "rust", "go", "ruby",
        "php", "html", "css", "sql", "mongodb", "firebase",
        "aws", "docker", "kubernetes", "streamlit", "fastapi",
    ]
    text_lower = text.lower()
    found = [kw for kw in tech_keywords if kw in text_lower]
    return ", ".join(found) if found else "General"


def scrape_multiple_urls(urls):
    """Scrape multiple URLs and return combined project list."""
    all_projects = []
    for url in urls:
        projects = scrape_project_ideas(url)
        all_projects.extend(projects)
        logger.info(f"Scraped {len(projects)} projects from {url}")
    return all_projects
