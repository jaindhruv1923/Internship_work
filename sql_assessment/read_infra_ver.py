dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

# Search for INSERT INTO `infrastructure_version`
pos = 0
with open(dump_path, 'rb') as f:
    chunk_size = 64 * 1024 * 1024
    offset = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        idx = chunk.find(b"INSERT INTO `infrastructure_version`")
        if idx != -1:
            pos = offset + idx
            break
        offset += len(chunk)

print(f"infrastructure_version insert at {pos}")
with open(dump_path, 'rb') as f:
    f.seek(pos)
    data = f.read(500000).decode('utf-8', errors='ignore')

import re
# find 239 and 240
for m in re.finditer(r"\((239|240),[^;]+?\)", data):
    print(m.group(0))
