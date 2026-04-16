#!/usr/bin/env python3
"""NBFIRA Botswana Regulator Entities Scraper"""

import re
import csv
import urllib.request
import time
import sys
import gzip
from html import unescape

BASE_URLS = {
    "lending": "https://www.nbfira.org.bw/list-of-regulated-entities/lending-activities-entities/",
    "insurance": "https://www.nbfira.org.bw/list-of-regulated-entities/insurance-licenced-entities/",
    "retirement": "https://www.nbfira.org.bw/list-of-regulated-entities/retirement-funds-entities/",
}

def fetch_page(category, page_num):
    """Fetch a single page"""
    url = f"{BASE_URLS[category]}page/{page_num}/"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Encoding': 'gzip, deflate'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            # Handle gzip encoding
            if response.info().get('Content-Encoding') == 'gzip':
                data = gzip.decompress(data)
            return data.decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return ""

def parse_page(html):
    """Parse entities from page HTML"""
    entities = []
    
    # Match table rows with entity data
    # Pattern: <tr ...>...<td>1</td><td>Entity Name</td><td>Sector</td>
    pattern = r'<tr[^>]*>\s*<td>([0-9]+)</td>\s*<td>([^<]+)</td>\s*<td>([^<]+)</td>'
    
    for match in re.finditer(pattern, html, re.MULTILINE | re.DOTALL):
        num = match.group(1).strip()
        name = unescape(match.group(2).strip())
        sector = unescape(match.group(3).strip())
        if name and name != '&nbsp;':
            entities.append({
                'number': num,
                'name': name,
                'sector': sector
            })
    
    return entities

def find_total_pages(html):
    """Find total pages from HTML"""
    # Check for pagination showing "... 25 ..."
    match = re.search(r'href="page/([0-9]+)/"', html)
    if match:
        return int(match.group(1))
    return 1

def scrape_category(category, output_file):
    """Scrape all entities for a category"""
    print(f"Scraping {category}...")
    
    # First, get page 1 to determine structure
    html = fetch_page(category, 1)
    if not html:
        print(f"Failed to fetch page 1", file=sys.stderr)
        return 0
    
    entities = parse_page(html)
    print(f"Page 1: {len(entities)} entities")
    
    # Find total pages
    max_page = 1
    for match in re.finditer(r'page/([0-9]+)/"', html):
        max_page = max(max_page, int(match.group(1)))
    
    print(f"Total pages: {max_page}")
    
    # Fetch remaining pages
    all_entities = entities
    for page in range(2, max_page + 1):
        time.sleep(0.2)  # Be respectful
        html = fetch_page(category, page)
        entities = parse_page(html)
        all_entities.extend(entities)
        print(f"Page {page}: {len(entities)} entities, total: {len(all_entities)}")
    
    # Remove duplicates by number
    seen = set()
    unique = []
    for e in all_entities:
        if e['number'] not in seen:
            seen.add(e['number'])
            unique.append(e)
    
    # Write CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['number', 'name', 'sector'])
        writer.writeheader()
        for e in unique:
            writer.writerow(e)
    
    print(f"Wrote {len(unique)} unique entities to {output_file}")
    return len(unique)

if __name__ == "__main__":
    total = 0
    for cat, url in BASE_URLS.items():
        output = f"nbfira_{cat}.csv"
        count = scrape_category(cat, output)
        total += count
    print(f"\nTotal: {total} entities")