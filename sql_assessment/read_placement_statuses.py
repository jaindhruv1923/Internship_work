dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

# Search for INSERT INTO `placement_application_status`
with open(dump_path, 'rb') as f:
    chunk_size = 64 * 1024 * 1024
    offset = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        idx = chunk.find(b"INSERT INTO `placement_application_status`")
        if idx != -1:
            print("placement_application_status at", offset + idx)
            f.seek(offset + idx)
            print(f.read(2000).decode('utf-8', errors='ignore'))
            break
        offset += len(chunk)

with open(dump_path, 'rb') as f:
    chunk_size = 64 * 1024 * 1024
    offset = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        idx = chunk.find(b"INSERT INTO `placement_offer_status`")
        if idx != -1:
            print("placement_offer_status at", offset + idx)
            f.seek(offset + idx)
            print(f.read(1000).decode('utf-8', errors='ignore'))
            break
        offset += len(chunk)
