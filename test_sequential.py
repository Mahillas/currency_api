#!/usr/bin/env python3
import urllib.request
import re
import time

base_url = "https://www.ncr.org.za/register_of_registrants/registered_cp.php"

all_ids = set()
for page in range(10):
    url = f"{base_url}?page={page}"
    time.sleep(0.1)  # 100ms delay
    html = urllib.request.urlopen(url).read().decode()
    ids = set(re.findall(r'NCRCP(\d+)', html))
    all_ids.update(ids)
    print(f"Page {page}: {len(ids)} new, total: {len(all_ids)}")

print(f"\nTotal unique: {len(all_ids)}")
print(f"Expected: 9682")