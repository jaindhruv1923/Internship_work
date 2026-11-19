import re

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

def inspect_table_data(target_table, limit=5):
    print(f"=== Sample data for {target_table} ===")
    count = 0
    with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
        in_insert = False
        for line in f:
            if line.startswith(f"INSERT INTO `{target_table}`") or line.startswith(f"INSERT INTO {target_table}"):
                print(line[:500])
                count += 1
                if count >= limit:
                    break

inspect_table_data("hostel_allotment", 2)
inspect_table_data("infrastructure_master", 2)
inspect_table_data("infrastructure_version", 2)
inspect_table_data("infrastructure_type", 10)
