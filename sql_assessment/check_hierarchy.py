import re

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"

# Let's search for INSERT INTO hostel_option_selection and check if building_id is populated
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith("INSERT INTO `hostel_option_selection`") or line.startswith("INSERT INTO hostel_option_selection"):
            print("Found hostel_option_selection insert!")
            print(line[:300])
            break

# Also check infrastructure_type values
types = []
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith("INSERT INTO `infrastructure_type`") or line.startswith("INSERT INTO infrastructure_type"):
            print("Found infrastructure_type insert!")
            print(line[:400])
            break
