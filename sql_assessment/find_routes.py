import re

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"
patterns = ['route', 'pickup', 'vehicle', 'seat', 'v2']
found = set()
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith('CREATE TABLE'):
            m = re.search(r"CREATE TABLE [`'\"]?([a-zA-Z0-9_]+)[`'\"]?", line)
            if m:
                tbl = m.group(1).lower()
                for p in patterns:
                    if p in tbl:
                        found.add(tbl)

for t in sorted(found):
    print(t)
