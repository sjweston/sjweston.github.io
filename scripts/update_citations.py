#!/usr/bin/env python3
"""
Fetch citation data from Semantic Scholar API and update publication files.
Falls back to scholarly (Google Scholar scraper) for papers not found.

Usage:
    python scripts/update_citations.py

Environment variables:
    SEMANTIC_SCHOLAR_API_KEY (optional): API key for higher rate limits
"""

import os
import json
import time
import re
import yaml
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

# Configuration
ORCID = "0000-0001-7782-6239"  # Sara Weston's ORCID
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
CONTENT_DIR = Path(__file__).parent.parent / "content" / "publication"
DATA_DIR = Path(__file__).parent.parent / "data"
METRICS_FILE = DATA_DIR / "metrics.json"

# Rate limiting
REQUEST_DELAY = 1.0  # seconds between requests (be nice to the API)


def get_semantic_scholar_headers() -> Dict[str, str]:
    """Get headers for Semantic Scholar API requests."""
    headers = {"Accept": "application/json"}
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key
    return headers


def fetch_author_papers_semantic_scholar(orcid: str) -> List[Dict[str, Any]]:
    """Fetch all papers for an author from Semantic Scholar using ORCID."""
    print(f"Fetching papers from Semantic Scholar for ORCID: {orcid}")

    # First, get the author ID from ORCID
    url = f"{SEMANTIC_SCHOLAR_API}/author/ORCID:{orcid}"
    params = {"fields": "authorId,name,paperCount,citationCount,hIndex"}

    try:
        response = requests.get(url, headers=get_semantic_scholar_headers(), params=params)
        response.raise_for_status()
        author_data = response.json()
        author_id = author_data.get("authorId")

        print(f"Found author: {author_data.get('name')} (ID: {author_id})")
        print(f"Total citations: {author_data.get('citationCount')}, h-index: {author_data.get('hIndex')}")

        # Save author metrics
        metrics = {
            "total_citations": author_data.get("citationCount", 0),
            "h_index": author_data.get("hIndex", 0),
            "paper_count": author_data.get("paperCount", 0),
            "last_updated": datetime.now().isoformat(),
            "source": "semantic_scholar"
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching author data: {e}")
        return [], {}

    time.sleep(REQUEST_DELAY)

    # Now fetch all papers
    papers = []
    offset = 0
    limit = 100

    while True:
        url = f"{SEMANTIC_SCHOLAR_API}/author/{author_id}/papers"
        params = {
            "fields": "paperId,title,year,citationCount,externalIds,publicationDate",
            "offset": offset,
            "limit": limit
        }

        try:
            response = requests.get(url, headers=get_semantic_scholar_headers(), params=params)
            response.raise_for_status()
            data = response.json()

            batch = data.get("data", [])
            papers.extend(batch)

            print(f"Fetched {len(batch)} papers (total: {len(papers)})")

            if len(batch) < limit:
                break

            offset += limit
            time.sleep(REQUEST_DELAY)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching papers: {e}")
            break

    return papers, metrics


def fetch_from_scholarly(title: str) -> Optional[Dict[str, Any]]:
    """Fallback: fetch citation data from Google Scholar using scholarly."""
    try:
        from scholarly import scholarly

        print(f"  Trying scholarly for: {title[:50]}...")
        search = scholarly.search_pubs(title)
        pub = next(search, None)

        if pub:
            return {
                "citationCount": pub.get("num_citations", 0),
                "source": "google_scholar"
            }
    except ImportError:
        print("  scholarly not installed, skipping Google Scholar fallback")
    except Exception as e:
        print(f"  scholarly error: {e}")

    return None


def normalize_title(title: str) -> str:
    """Normalize a title for comparison."""
    # Remove punctuation, lowercase, remove extra spaces
    title = re.sub(r'[^\w\s]', '', title.lower())
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def match_paper_to_publication(paper: Dict[str, Any], pub_titles: Dict[str, Path]) -> Optional[Path]:
    """Try to match a Semantic Scholar paper to a local publication file."""
    paper_title = normalize_title(paper.get("title", ""))

    # Direct match
    if paper_title in pub_titles:
        return pub_titles[paper_title]

    # Fuzzy match (title contains or is contained)
    for local_title, path in pub_titles.items():
        if paper_title in local_title or local_title in paper_title:
            return path
        # Check if most words match
        paper_words = set(paper_title.split())
        local_words = set(local_title.split())
        if len(paper_words) > 3 and len(local_words) > 3:
            overlap = len(paper_words & local_words) / max(len(paper_words), len(local_words))
            if overlap > 0.7:
                return path

    return None


def load_publication_frontmatter(filepath: Path) -> Dict[str, Any]:
    """Load YAML frontmatter from a publication markdown file."""
    content = filepath.read_text(encoding='utf-8')

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1])
            except yaml.YAMLError:
                pass
    return {}


def update_publication_citations(filepath: Path, citations: int, source: str):
    """Update the citation count in a publication's frontmatter."""
    content = filepath.read_text(encoding='utf-8')

    if not content.startswith('---'):
        print(f"  Skipping {filepath.name}: no frontmatter")
        return

    parts = content.split('---', 2)
    if len(parts) < 3:
        return

    try:
        frontmatter = yaml.safe_load(parts[1])
        if frontmatter is None:
            frontmatter = {}
    except yaml.YAMLError:
        return

    # Update citation data
    old_citations = frontmatter.get('citation_count', 0)
    frontmatter['citation_count'] = citations
    frontmatter['citation_source'] = source
    frontmatter['citation_updated'] = datetime.now().strftime('%Y-%m-%d')

    # Rebuild the file
    new_frontmatter = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    new_content = f"---\n{new_frontmatter}---{parts[2]}"

    filepath.write_text(new_content, encoding='utf-8')

    if old_citations != citations:
        print(f"  Updated {filepath.name}: {old_citations} -> {citations} citations")
    else:
        print(f"  {filepath.name}: {citations} citations (unchanged)")


def get_local_publications() -> Dict[str, Path]:
    """Get all local publication files and their normalized titles."""
    pub_titles = {}

    for pub_dir in CONTENT_DIR.iterdir():
        if pub_dir.is_dir():
            index_file = pub_dir / "index.md"
            if index_file.exists():
                frontmatter = load_publication_frontmatter(index_file)
                title = frontmatter.get("title", "")
                if title:
                    pub_titles[normalize_title(title)] = index_file

    return pub_titles


def main():
    print("=" * 60)
    print("Citation Update Script")
    print("=" * 60)
    print()

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Fetch papers from Semantic Scholar
    papers, metrics = fetch_author_papers_semantic_scholar(ORCID)

    if not papers:
        print("No papers found from Semantic Scholar")
        # Try to load existing metrics
        if METRICS_FILE.exists():
            metrics = json.loads(METRICS_FILE.read_text())

    # Get local publications
    print("\nLoading local publications...")
    pub_titles = get_local_publications()
    print(f"Found {len(pub_titles)} local publications")

    # Match and update
    print("\nMatching papers to local publications...")
    matched = 0
    unmatched_papers = []
    total_local_citations = 0

    for paper in papers:
        filepath = match_paper_to_publication(paper, pub_titles)
        if filepath:
            citations = paper.get("citationCount", 0)
            update_publication_citations(filepath, citations, "semantic_scholar")
            matched += 1
            total_local_citations += citations
        else:
            unmatched_papers.append(paper)

    print(f"\nMatched {matched}/{len(papers)} papers")

    # Try scholarly for unmatched local publications
    print("\nChecking for unmatched local publications...")
    matched_titles = {normalize_title(p.get("title", "")) for p in papers if match_paper_to_publication(p, pub_titles)}

    for title, filepath in pub_titles.items():
        if title not in matched_titles:
            frontmatter = load_publication_frontmatter(filepath)
            original_title = frontmatter.get("title", "")
            print(f"  Unmatched: {original_title[:50]}...")

            # Try scholarly as fallback
            scholar_data = fetch_from_scholarly(original_title)
            if scholar_data:
                update_publication_citations(
                    filepath,
                    scholar_data["citationCount"],
                    scholar_data["source"]
                )
                total_local_citations += scholar_data["citationCount"]
            time.sleep(REQUEST_DELAY * 2)  # Extra delay for scholarly

    # Update metrics with local citation total
    metrics["local_citation_total"] = total_local_citations
    metrics["publications_tracked"] = len(pub_titles)

    # Save metrics
    print(f"\nSaving metrics to {METRICS_FILE}")
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total citations (Semantic Scholar): {metrics.get('total_citations', 'N/A')}")
    print(f"h-index: {metrics.get('h_index', 'N/A')}")
    print(f"Papers in Semantic Scholar: {metrics.get('paper_count', 'N/A')}")
    print(f"Local publications tracked: {metrics.get('publications_tracked', 0)}")
    print(f"Last updated: {metrics.get('last_updated', 'N/A')}")
    print()


if __name__ == "__main__":
    main()
