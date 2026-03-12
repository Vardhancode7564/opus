"""GitHub Project Collector - Fetches student project repositories via GitHub API."""

import requests
import time
import logging

from config import GITHUB_API_URL, GITHUB_TOKEN

logger = logging.getLogger(__name__)


def _get_headers():
    """Build request headers, with auth token if available."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers


# Multiple query variations to get diverse results instead of the same top repos
QUERY_VARIATIONS = [
    "{query}",
    "{query} final year",
    "{query} capstone",
    "{query} mini project",
    "{query} college",
    "{query} academic",
    "{query} semester",
    "{query} undergraduate",
]


def search_github_repos(query="student project", max_results=30):
    """
    Search GitHub for repositories matching the query.
    Uses authenticated requests and multiple query variations to get diverse results.
    Returns a list of project dicts with title, description, language, readme, link.
    """
    projects = []
    seen_ids = set()  # track repo IDs to avoid duplicates across queries
    headers = _get_headers()

    # Distribute max_results across query variations
    per_query = max(5, max_results // len(QUERY_VARIATIONS))

    for query_template in QUERY_VARIATIONS:
        if len(projects) >= max_results:
            break

        search_query = query_template.format(query=query)
        page = 1

        while len(projects) < max_results:
            params = {
                "q": search_query,
                "sort": "updated",
                "order": "desc",
                "per_page": 30,
                "page": page,
            }
            try:
                resp = requests.get(
                    f"{GITHUB_API_URL}/search/repositories",
                    params=params,
                    headers=headers,
                    timeout=15,
                )
                if resp.status_code == 403:
                    remaining = resp.headers.get("X-RateLimit-Remaining", "?")
                    logger.warning(f"GitHub rate limit hit (remaining: {remaining}). Trying next query.")
                    break
                if resp.status_code == 422:
                    break  # invalid query
                resp.raise_for_status()
                data = resp.json()
                items = data.get("items", [])
                if not items:
                    break

                new_in_page = 0
                for repo in items:
                    repo_id = repo.get("id")
                    if repo_id in seen_ids:
                        continue
                    seen_ids.add(repo_id)

                    # Skip repos with no description
                    desc = repo.get("description", "") or ""
                    if not desc:
                        continue

                    readme_content = _fetch_readme(repo["full_name"], headers)

                    # Collect topics as extra tech info
                    topics = repo.get("topics", []) or []
                    language = repo.get("language", "") or ""
                    tech_parts = [language] if language else []
                    tech_parts.extend(topics[:5])
                    technologies = ", ".join(tech_parts) if tech_parts else "General"

                    project = {
                        "project_title": repo.get("name", ""),
                        "description": desc,
                        "technologies": technologies,
                        "source": "github",
                        "project_link": repo.get("html_url", ""),
                        "readme": readme_content,
                    }
                    projects.append(project)
                    new_in_page += 1

                    if len(projects) >= max_results:
                        break

                # If we got enough from this query variation, move on
                if new_in_page == 0 or len(projects) >= len(seen_ids) >= per_query:
                    break

                page += 1
                time.sleep(0.5 if GITHUB_TOKEN else 2)

            except requests.RequestException as e:
                logger.error(f"GitHub API error for query '{search_query}': {e}")
                break

        time.sleep(0.3 if GITHUB_TOKEN else 1)

    logger.info(f"Fetched {len(projects)} unique projects from GitHub")
    return projects[:max_results]


def _fetch_readme(full_name, headers=None):
    """Fetch the README content for a repository."""
    if headers is None:
        headers = _get_headers()
    try:
        readme_headers = {**headers, "Accept": "application/vnd.github.v3.raw"}
        resp = requests.get(
            f"{GITHUB_API_URL}/repos/{full_name}/readme",
            headers=readme_headers,
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.text[:2000]
    except requests.RequestException:
        pass
    return ""


def fetch_repo_details(repo_url):
    """Fetch details for a single GitHub repository URL."""
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2:
        return None
    owner, repo = parts[-2], parts[-1]
    headers = _get_headers()

    try:
        resp = requests.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}",
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        readme = _fetch_readme(f"{owner}/{repo}", headers)

        language = data.get("language", "") or ""
        topics = data.get("topics", []) or []
        tech_parts = [language] if language else []
        tech_parts.extend(topics[:5])
        technologies = ", ".join(tech_parts) if tech_parts else "General"

        return {
            "project_title": data.get("name", ""),
            "description": data.get("description", "") or "",
            "technologies": technologies,
            "source": "github",
            "project_link": data.get("html_url", ""),
            "readme": readme,
        }
    except requests.RequestException as e:
        logger.error(f"Error fetching repo {repo_url}: {e}")
        return None
