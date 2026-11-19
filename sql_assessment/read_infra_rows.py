dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

# Read 50KB around byte 7867567448 to see infrastructure_master rows
with open(dump_path, 'rb') as f:
    f.seek(7867567448)
    data = f.read(100000).decode('utf-8', errors='ignore')

# Print first 20 rows
import re
rows = re.findall(r"\([0-9]+,[^;]+?\)", data)
for r in rows[:25]:
    print(r)
