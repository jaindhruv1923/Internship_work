import re

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

# Check infrastructure_type values
pos = 7867816680
with open(dump_path, 'rb') as f:
    f.seek(pos)
    data = f.read(10000).decode('utf-8', errors='ignore')

# print type id and type name
for m in re.finditer(r"\(([0-9]+),'([^']+)'", data):
    print(m.group(1), m.group(2))
