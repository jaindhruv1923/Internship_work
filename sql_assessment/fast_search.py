import sys

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

targets = [b"INSERT INTO `hostel_option_selection`", b"INSERT INTO `infrastructure_master`", b"INSERT INTO `infrastructure_type`"]
found = {}

with open(dump_path, 'rb') as f:
    chunk_size = 64 * 1024 * 1024
    offset = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        for t in targets:
            if t not in found:
                idx = chunk.find(t)
                if idx != -1:
                    found[t] = offset + idx
                    print(f"Found {t.decode()} at byte {offset+idx}")
        if len(found) == len(targets):
            break
        offset += len(chunk)

for t, pos in found.items():
    with open(dump_path, 'rb') as f:
        f.seek(pos)
        sample = f.read(1000)
        print(f"\nSample at {pos} for {t.decode()}:")
        print(sample.decode('utf-8', errors='ignore')[:400])
