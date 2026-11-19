import re
from collections import defaultdict

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

# Load infrastructure_version names and parents
# iv_id -> (name, parent_id)
iv_data = {}
pos = 7867834958
with open(dump_path, 'rb') as f:
    f.seek(pos)
    # read until end of iv insert
    data = f.read(2000000).decode('utf-8', errors='ignore')

# parse rows: (id, name, college_id, ..., parent_id, ...)
# Let's see how many rows
for m in re.finditer(r"\(([0-9]+),'([^']*)',([0-9]+),[^;]+?\)", data):
    # let's parse more carefully
    pass

# Let's test with regex for parent_id:
# In iv: id, name, college_id, ... 25th field is parent_id
print("Done parsing check")
