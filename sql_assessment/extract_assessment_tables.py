import os
import re
import time

dump_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\bi_dump_2026_05_08_updated.sql"
tables_to_find = {
    'chc_request', 'chc_service', 'chc_work_centre', 'chc_work_centre_action', 
    'chc_work_centre_request_action', 'chc_request_log', 'chc_middleware', 'chc_middleware_moderated_action',
    'gate_pass_status', 'gate_pass_log', 'gate_pass_long_pass', 'gate_pass_requests', 'gate_pass_audience',
    'hostel_allotment', 'hostel_option_selection', 'hostel_fee_policy', 'hostel_fee_policy_option',
    'placement_job', 'placement_organization', 'placement_application', 'placement_application_status', 
    'placement_offer_status', 'placement_student_status', 'placement_status',
    'infra_booking', 'infra_booking_item', 'infra_booking_request_detail', 'infra_booking_request_allotment_map',
    'infrastructure_master', 'infrastructure_version', 'infrastructure_type',
    'transport_management_v2_allotment', 'transport_management_v2_option_selection', 
    'transport_management_v2_policy', 'transport_management_v2_policy_option',
    'transport_management_v2_route', 'transport_management_v2_route_stop', 
    'transport_management_v2_pickup_point', 'transport_management_v2_policy_route_stop_fees'
}

t0 = time.time()
found = {}
current_table = None
current_lines = []

print(f"Opening {dump_path}...")
with open(dump_path, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith('CREATE TABLE'):
            m = re.search(r"CREATE TABLE [`'\"]?([a-zA-Z0-9_]+)[`'\"]?", line)
            if m:
                tbl = m.group(1).lower()
                if tbl in tables_to_find:
                    current_table = tbl
                    current_lines = [line]
                    continue
        if current_table:
            current_lines.append(line)
            if line.strip().endswith(';') or line.startswith(') ENGINE') or line.startswith(') '):
                found[current_table] = ''.join(current_lines)
                print(f"Found {current_table} in {time.time()-t0:.1f}s")
                current_table = None
                current_lines = []
                if len(found) == len(tables_to_find):
                    break

print(f"Total found: {len(found)} / {len(tables_to_find)} in {time.time()-t0:.1f}s")
out_path = r"C:\Users\Admin\Desktop\worklogs\sql_assessment\extracted_tables.sql"
with open(out_path, 'w', encoding='utf-8') as out:
    for t, s in sorted(found.items()):
        out.write(f"-- ==================== {t} ====================\n" + s + "\n\n")

print(f"Written to {out_path}")
