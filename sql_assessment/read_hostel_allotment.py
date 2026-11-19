dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

# Let's search for hostel_allotment rows
pos = 0
with open(dump_path, 'rb') as f:
    chunk_size = 64 * 1024 * 1024
    offset = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        idx = chunk.find(b"INSERT INTO `hostel_allotment`")
        if idx != -1:
            pos = offset + idx
            break
        offset += len(chunk)

print(f"hostel_allotment insert at {pos}")
with open(dump_path, 'rb') as f:
    f.seek(pos)
    data = f.read(50000).decode('utf-8', errors='ignore')

import re
rows = re.findall(r"\([0-9]+,[^;]+?\)", data)
for r in rows[:10]:
    print(r)
