import re

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"
transport_tables = []
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith('CREATE TABLE'):
            m = re.search(r"CREATE TABLE [`'\"]?([a-zA-Z0-9_]+)[`'\"]?", line)
            if m:
                tbl = m.group(1).lower()
                if 'transport' in tbl:
                    transport_tables.append(tbl)
                    print(tbl)

print("Found tables:", transport_tables)
