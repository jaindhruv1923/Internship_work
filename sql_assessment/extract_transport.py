import re

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"
tables = [
    'fee_consolidated_transport_option', 'transport_allotment', 'transport_fee_policy', 
    'transport_management_settings', 'transport_option_selection', 'transport_pickup_point', 
    'transport_route', 'transport_route_category', 'transport_route_filter', 
    'transport_route_pickup_point', 'transport_route_registration'
]

found = {}
current_table = None
current_lines = []

with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith('CREATE TABLE'):
            m = re.search(r"CREATE TABLE [`'\"]?([a-zA-Z0-9_]+)[`'\"]?", line)
            if m:
                tbl = m.group(1).lower()
                if tbl in tables:
                    current_table = tbl
                    current_lines = [line]
                    continue
        if current_table:
            current_lines.append(line)
            if line.strip().endswith(';') or line.startswith(') ENGINE') or line.startswith(') '):
                found[current_table] = ''.join(current_lines)
                current_table = None
                current_lines = []
                if len(found) == len(tables):
                    break

out_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\extracted_transport_v1.sql"
with open(out_path, 'w', encoding='utf-8') as out:
    for t, s in sorted(found.items()):
        out.write(f"-- ==================== {t} ====================\n" + s + "\n\n")

print(f"Extracted {len(found)} tables to {out_path}")
