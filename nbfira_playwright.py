#!/usr/bin/env python3
"""
NBFIRA Botswana Scraper using Playwright for JS rendering
"""

import asyncio
import csv
import re
from playwright.async_api import async_playwright

BASE_URLS = {
    "lending": "https://www.nbfira.org.bw/list-of-regulated-entities/lending-activities-entities/",
    "insurance": "https://www.nbfira.org.bw/list-of-regulated-entities/insurance-licenced-entities/",
    "retirement": "https://www.nbfira.org.bw/list-of-regulated-entities/retirement-funds-entities/",
}

async def scrape_page(page, url):
    """Scrape entities from a single page"""
    entities = []
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Wait for table to load
        await page.wait_for_selector('table tbody tr', timeout=10000)
        
        # Get all table rows
        rows = await page.query_selector_all('table tbody tr')
        
        for row in rows:
            tds = await row.query_selector_all('td')
            if len(tds) >= 3:
                num = await tds[0].inner_text()
                name = await tds[1].inner_text()
                sector = await tds[2].inner_text()
                
                num = num.strip()
                name = name.strip()
                sector = sector.strip()
                
                if num.isdigit():
                    entities.append({
                        'number': num,
                        'name': name,
                        'sector': sector
                    })
    except Exception as e:
        print(f"Error: {e}")
    
    return entities

async def get_total_pages(page, base_url):
    """Get the last page number"""
    try:
        await page.goto(base_url, wait_until="networkidle", timeout=30000)
        await page.wait_for_selector('.pagination a', timeout=5000)
        
        # Find all page links
        page_links = await page.query_selector_all('.pagination a')
        
        max_page = 1
        for link in page_links:
            text = await link.inner_text()
            if text.isdigit():
                max_page = max(max_page, int(text))
        
        return max_page
    except:
        return 1

async def scrape_category(category, base_url, output_file):
    """Scrape all entities for a category"""
    print(f"Scraping {category}...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Get total pages
        print(f"Getting total pages...")
        max_page = await get_total_pages(page, base_url)
        print(f"Total pages: {max_page}")
        
        # Scrape all pages
        all_entities = []
        for page_num in range(1, max_page + 1):
            url = f"{base_url}page/{page_num}/" if page_num > 1 else base_url
            print(f"Page {page_num}/{max_page}...")
            
            entities = await scrape_page(page, url)
            all_entities.extend(entities)
            print(f"  Found {len(entities)} entities, total: {len(all_entities)}")
        
        await browser.close()
        
        # Deduplicate
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
        
        print(f"Wrote {len(unique)} entities to {output_file}")
        return len(unique)

async def main():
    total = 0
    for cat, url in BASE_URLS.items():
        output = f"nbfira_{cat}.csv"
        count = await scrape_category(cat, url, output)
        total += count
    print(f"\nTotal: {total} entities")

if __name__ == "__main__":
    asyncio.run(main())