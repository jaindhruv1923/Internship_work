dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

# Search for INSERT INTO `chc_work_centre_request_action`
with open(dump_path, 'rb') as f:
    chunk_size = 64 * 1024 * 1024
    offset = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        idx = chunk.find(b"INSERT INTO `chc_work_centre_request_action`")
        if idx != -1:
            print("chc_work_centre_request_action at", offset + idx)
            f.seek(offset + idx)
            print(f.read(600).decode('utf-8', errors='ignore'))
            break
        offset += len(chunk)
