#!/usr/bin/env python3
import urllib.request
import re

# Check page 0 to see record count
url0 = 'https://www.ncr.org.za/register_of_registrants/registered_cp.php?page=0'
html0 = urllib.request.urlopen(url0).read().decode()
m0 = re.findall(r'NCRCP\d+', html0)
rec_count = re.search(r'Records found: (\d+)', html0)
print('Page 0 records shown:', rec_count.group(1) if rec_count else '?')
print('Page 0 unique NCRCPs:', len(set(m0)))

# Check page 1
url1 = 'https://www.ncr.org.za/register_of_registrants/registered_cp.php?page=1'
html1 = urllib.request.urlopen(url1).read().decode()
m1 = set(re.findall(r'NCRCP\d+', html1))
print('Page1 unique NCRCPs:', len(m1))

# With 20 records per page and 9682 total, need ~485 pages
print('Estimated pages needed:', 9682 // 20 + 1)