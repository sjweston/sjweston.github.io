#!/usr/bin/env python3
"""
Script to create missing publication folders from publications.bib
"""

import os
import re
from pathlib import Path

# Base paths
BASE_DIR = Path("/Users/sweston2/Documents/GitHub/sjweston.github.io")
PUB_DIR = BASE_DIR / "content" / "publication"
BIB_FILE = BASE_DIR / "publications.bib"

# Get existing publication folders
existing_folders = set()
for item in PUB_DIR.iterdir():
    if item.is_dir() and not item.name.startswith('_'):
        existing_folders.add(item.name)

print(f"Found {len(existing_folders)} existing publication folders:")
for f in sorted(existing_folders):
    print(f"  - {f}")

# Parse bibtex file
with open(BIB_FILE, 'r') as f:
    bib_content = f.read()

# Split into individual entries
entries = re.split(r'\n(?=@)', bib_content.strip())

def parse_bib_entry(entry):
    """Parse a single bibtex entry into a dictionary."""
    if not entry.strip():
        return None

    # Get entry type and key
    match = re.match(r'@(\w+)\{([^,]+),', entry)
    if not match:
        return None

    entry_type = match.group(1).lower()
    key = match.group(2).strip()

    # Parse fields
    fields = {}
    # Match field = {value} or field = value
    field_pattern = r'(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
    for m in re.finditer(field_pattern, entry):
        field_name = m.group(1).lower()
        field_value = m.group(2).strip()
        fields[field_name] = field_value

    return {
        'type': entry_type,
        'key': key,
        'fields': fields,
        'raw': entry
    }

def key_to_folder_name(key):
    """Convert bibtex key to folder name."""
    # Replace underscores with hyphens, handle special cases
    folder = key.replace('_', '-').lower()
    # Remove trailing -1, -2 etc for duplicates
    folder = re.sub(r'-(\d+)$', '', folder)
    return folder

def format_authors(author_str):
    """Convert bibtex author format to YAML list."""
    if not author_str:
        return []
    # Split on " and "
    authors = re.split(r'\s+and\s+', author_str)
    formatted = []
    for author in authors:
        author = author.strip()
        # Handle "Last, First" format
        if ',' in author:
            parts = author.split(',', 1)
            author = f"{parts[1].strip()} {parts[0].strip()}"
        # Handle {others}
        if author.lower() == '{others}' or author.lower() == 'others':
            continue
        formatted.append(author)
    return formatted

def get_publication_type(entry_type):
    """Map bibtex type to Hugo publication type."""
    type_map = {
        'article': 'article-journal',
        'incollection': 'chapter',
        'inproceedings': 'paper-conference',
        'book': 'book',
        'phdthesis': 'thesis',
        'mastersthesis': 'thesis',
        'techreport': 'report',
    }
    return type_map.get(entry_type, 'article-journal')

def create_index_md(entry):
    """Create the index.md content for a publication."""
    fields = entry['fields']

    title = fields.get('title', 'Untitled')
    # Clean up title
    title = re.sub(r'\{|\}', '', title)
    title = title.replace('\n', ' ').strip()

    authors = format_authors(fields.get('author', ''))
    year = fields.get('year', '2024')
    journal = fields.get('journal', fields.get('booktitle', ''))
    journal = re.sub(r'\{|\}', '', journal)
    journal = journal.replace('\\&', '&')

    doi = fields.get('doi', '')
    abstract = fields.get('abstract', '')
    abstract = re.sub(r'\{|\}', '', abstract)
    abstract = abstract.replace('\n', ' ').strip()

    pub_type = get_publication_type(entry['type'])

    # Build YAML
    lines = ['---']

    # Handle title with special characters
    if ':' in title or "'" in title or '"' in title:
        lines.append(f"title: \"{title}\"")
    else:
        lines.append(f"title: '{title}'")

    # Authors
    lines.append('authors:')
    for author in authors:
        lines.append(f'- {author}')

    lines.append(f"date: '{year}-01-01'")
    lines.append(f"publishDate: '{year}-01-01T00:00:00Z'")
    lines.append('publication_types:')
    lines.append(f'- {pub_type}')

    if journal:
        lines.append(f"publication: '*{journal}*'")

    if doi:
        lines.append(f'doi: {doi}')

    if abstract:
        # Handle multiline abstract
        lines.append('abstract: |')
        # Wrap abstract at ~80 chars
        words = abstract.split()
        current_line = '  '
        for word in words:
            if len(current_line) + len(word) + 1 > 80:
                lines.append(current_line.rstrip())
                current_line = '  ' + word + ' '
            else:
                current_line += word + ' '
        if current_line.strip():
            lines.append(current_line.rstrip())

    lines.append('---')

    return '\n'.join(lines)

def create_cite_bib(entry):
    """Create the cite.bib content."""
    # Clean up the raw entry
    raw = entry['raw'].strip()
    # Remove file fields (local paths)
    raw = re.sub(r'\n\s*file\s*=\s*\{[^}]*\},?', '', raw)
    # Remove tex.ids
    raw = re.sub(r'\n\s*note\s*=\s*\{tex\.ids[^}]*\},?', '', raw)
    return raw + '\n'

# Process entries
print("\n\nProcessing bibtex entries...")
created = []
skipped = []

for entry_text in entries:
    entry = parse_bib_entry(entry_text)
    if not entry:
        continue

    folder_name = key_to_folder_name(entry['key'])

    # Check if folder exists (with some flexibility)
    folder_exists = False
    for existing in existing_folders:
        # Normalize for comparison
        existing_norm = existing.lower().replace('-', '')
        folder_norm = folder_name.lower().replace('-', '')
        if existing_norm == folder_norm or folder_name in existing or existing in folder_name:
            folder_exists = True
            break

    if folder_exists:
        skipped.append(folder_name)
        continue

    # Create folder
    folder_path = PUB_DIR / folder_name
    folder_path.mkdir(exist_ok=True)

    # Create index.md
    index_content = create_index_md(entry)
    with open(folder_path / 'index.md', 'w') as f:
        f.write(index_content)

    # Create cite.bib
    cite_content = create_cite_bib(entry)
    with open(folder_path / 'cite.bib', 'w') as f:
        f.write(cite_content)

    created.append(folder_name)
    print(f"  Created: {folder_name}")

print(f"\n\nSummary:")
print(f"  Created: {len(created)} new publication folders")
print(f"  Skipped: {len(skipped)} (already exist)")

if created:
    print("\nNew folders created:")
    for f in sorted(created):
        print(f"  - {f}")
