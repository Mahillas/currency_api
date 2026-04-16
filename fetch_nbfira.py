"""NBFIRA Botswana - fetch via AJAX API (no browser needed)"""
import csv
import urllib.request
import json

# Table IDs and their categories
TABLES = {
    "lending": {
        "url": "https://www.nbfira.org.bw/wp-admin/admin-ajax.php",
        "table_id": "10351",
        "nonce": "9576b1896e"
    },
    "insurance": {
        "url": "https://www.nbfira.org.bw/wp-admin/admin-ajax.php",
        "table_id": "10354", 
        "nonce": "9576b1896e"
    },
    "retirement": {
        "url": "https://www.nbfira.org.bw/wp-admin/admin-ajax.php",
        "table_id": "10350",
        "nonce": "9576b1896e"
    }
}

def fetch_table(category, info):
    """Fetch all data via AJAX"""
    params = (
        f"action=wp_ajax_ninja_tables_public_action"
        f"&table_id={info['table_id']}"
        f"&target_action=get-all-data"
        f"&default_sorting=old_first"
        f"&skip_rows=0"
        f"&limit_rows=0"
        f"&ninja_table_public_nonce={info['nonce']}"
    )
    
    url = f"{info['url']}?{params}"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0'
    })
    
    with urllib.request.urlopen(req) as response:
        data = json.load(response)
    
    # Parse records
    entities = []
    for row in data:
        val = row.get('value', {})
        entities.append({
            'number': val.get('no', ''),
            'name': val.get('licensed_entities', ''),
            'sector': val.get('sector', '')
        })
    
    return entities

# Fetch all
for cat, info in TABLES.items():
    print(f"Fetching {cat}...")
    entities = fetch_table(cat, info)
    print(f"  {len(entities)} records")
    
    # Write CSV
    with open(f'nbfira_{cat}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['number', 'name', 'sector'])
        writer.writeheader()
        writer.writerows(entities)
    
    print(f"  Wrote nbfira_{cat}.csv")

print("\nDone!")
