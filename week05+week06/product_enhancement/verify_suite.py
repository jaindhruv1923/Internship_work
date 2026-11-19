# -*- coding: utf-8 -*-
"""
Verification & Compliance Suite — Digii Campus 2.0
Audits:
1. SPA_VIEWS registry & HTML section synchronization (25 views)
2. Sidebar navigation link integrity (25 nav links)
3. DOM-ID uniqueness (zero duplicate element IDs)
4. Strict zero-emoji compliance (astral & BMP emoji symbols)
5. Inline event handler integrity (all inline event handlers defined in JS)
6. Executive tone & terminology (zero derogatory or legacy slang)
7. CHC architecture accuracy (Campus Help Centre service request engine)
8. Regulatory claim audit (zero occurrences of ISO 27001, FERPA, GDPR, HIPAA)
9. Data transparency banner (DPDP Act 2023 simulated cohort disclosure)
10. CollPoll production schema grounding (confirmed tables from schema definition)
11. No unhandled NaN / undefined in static UI text
12. Single-origin Python server status (port 8000)
"""
import re
import os
import sys
import urllib.request
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(SCRIPT_DIR, "index.html")

if not os.path.exists(HTML_PATH):
    print(f"FATAL: {HTML_PATH} does not exist.")
    sys.exit(1)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print("=" * 80)
print("DIGII CAMPUS 2.0 — VERIFICATION & COMPLIANCE SUITE")
print(f"Target: index.html ({len(html):,} bytes, {len(html.splitlines()):,} lines)")
print("=" * 80)

failures = []

# 1. SPA_VIEWS Registry
spa_match = re.search(r"const SPA_VIEWS = \[([^\]]+)\];", html)
if not spa_match:
    print("[1] SPA_VIEWS Registry: FAIL (const SPA_VIEWS not found)")
    failures.append("SPA_VIEWS missing")
else:
    views = [v.strip().strip("'\"") for v in spa_match.group(1).split(",") if v.strip()]
    print(f"[1] SPA_VIEWS Registry: PASS ({len(views)} views registered)")

# 2. HTML View Sections & Sidebar Nav Links
missing_sections = [v for v in views if f'id="view-{v}"' not in html]
missing_nav = [v for v in views if f'id="nav-{v}"' not in html]

if missing_sections:
    print(f"[2] HTML View Sections: FAIL (missing: {missing_sections})")
    failures.append(f"Missing HTML sections: {missing_sections}")
else:
    print(f"[2] HTML View Sections: PASS (all {len(views)} view containers present in DOM)")

if missing_nav:
    print(f"[3] Sidebar Navigation Links: FAIL (missing: {missing_nav})")
    failures.append(f"Missing sidebar links: {missing_nav}")
else:
    print(f"[3] Sidebar Navigation Links: PASS (all {len(views)} nav links present in sidebar)")

# 4. DOM-ID Uniqueness Check
dom_ids = re.findall(r'id=["\']([^"\']+)["\']', html)
id_counts = Counter(dom_ids)
duplicate_ids = {k: v for k, v in id_counts.items() if v > 1}
if duplicate_ids:
    print(f"[4] DOM ID Uniqueness: FAIL ({len(duplicate_ids)} duplicate IDs: {duplicate_ids})")
    failures.append(f"Duplicate DOM IDs: {duplicate_ids}")
else:
    print(f"[4] DOM ID Uniqueness: PASS (all {len(dom_ids)} element IDs are strictly unique)")

# 5. Strict Zero-Emoji Check (Astral and BMP symbols)
astral_emojis = re.findall(r'[\U00010000-\U0010ffff]', html)
bmp_emojis = re.findall(r'[\u2600-\u27bf]', html)
all_emojis = astral_emojis + bmp_emojis
if all_emojis:
    print(f"[5] Zero-Emoji Audit: FAIL ({len(all_emojis)} symbols found: {set(all_emojis)})")
    failures.append(f"Found {len(all_emojis)} emojis")
else:
    print("[5] Zero-Emoji Audit: PASS (0 emojis found; clean SVG icons only)")

# 6. Inline Event Handler Integrity
handler_patterns = [
    r'onclick="([a-zA-Z0-9_]+)\(',
    r'onchange="([a-zA-Z0-9_]+)\(',
    r'onsubmit="([a-zA-Z0-9_]+)\(',
    r'ondrop="([a-zA-Z0-9_]+)\(',
    r'ondragover="([a-zA-Z0-9_]+)\('
]
inline_calls = []
for pat in handler_patterns:
    inline_calls.extend(re.findall(pat, html))
unique_calls = sorted(set(inline_calls))

# Collect defined JS functions
js_funcs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html))
js_vars = set(re.findall(r'(?:const|let|var|window\.)([a-zA-Z0-9_]+)\s*=\s*(?:function|\([^)]*\)\s*=>)', html))
all_defined_funcs = js_funcs.union(js_vars)

# Standard browser globals or event methods that are valid
exempt_globals = {"event", "stopImmediatePropagation", "stopPropagation", "preventDefault"}
missing_handlers = [h for h in unique_calls if h not in all_defined_funcs and h not in exempt_globals]

if missing_handlers:
    print(f"[6] Event Handler Integrity: FAIL ({len(missing_handlers)} undefined handlers: {missing_handlers})")
    failures.append(f"Undefined event handlers: {missing_handlers}")
else:
    print(f"[6] Event Handler Integrity: PASS (all {len(unique_calls)} inline handlers defined in JS)")

# 7. Executive Tone & Terminology Check
tone_terms = ["POSH", "siloed nightmare", "clunky", "passive record"]
tone_matches = {term: len(re.findall(re.escape(term), html, re.I)) for term in tone_terms}
tone_failures = {t: c for t, c in tone_matches.items() if c > 0}
if tone_failures:
    print(f"[7] Executive Tone: FAIL ({tone_failures})")
    failures.append(f"Tone violations: {tone_failures}")
else:
    print("[7] Executive Tone: PASS (0 derogatory or clunky phrases)")

# 8. CHC Architecture Definition Check
chc_health_count = len(re.findall(r'Campus Health (?:Clinic|Center|Centre)', html, re.I))
chc_help_count = len(re.findall(r'Campus Help Centre', html, re.I))
if chc_health_count > 0:
    print(f"[8] CHC Definition: FAIL ('Campus Health' found {chc_health_count} times)")
    failures.append(f"CHC referred to as Campus Health {chc_health_count} times")
else:
    print(f"[8] CHC Definition: PASS (grounded as Campus Help Centre across {chc_help_count} occurrences)")

# 9. Regulatory Claims Audit (DPDP Act 2023 only; 0 ISO 27001 / FERPA / GDPR / HIPAA)
forbidden_regs = ["ISO 27001", "FERPA", "GDPR", "HIPAA"]
reg_findings = {reg: len(re.findall(re.escape(reg), html, re.I)) for reg in forbidden_regs}
reg_fails = {r: c for r, c in reg_findings.items() if c > 0}
if reg_fails:
    print(f"[9] Regulatory Claims: FAIL (unsubstantiated claims found: {reg_fails})")
    failures.append(f"Forbidden regulatory claims: {reg_fails}")
else:
    print("[9] Regulatory Claims: PASS (0 occurrences of ISO 27001, FERPA, GDPR, HIPAA; aligned to DPDP Act 2023)")

# 10. Data Transparency Banner
if "Simulated Enterprise Cohort" in html and "DPDP Act 2023" in html:
    print("[10] Data Transparency Banner: PASS (DPDP Act 2023 simulated cohort banner present)")
else:
    print("[10] Data Transparency Banner: FAIL (Missing or incomplete disclosure banner)")
    failures.append("Missing transparency banner")

# 11. CollPoll Production Schema Grounding Check
schema_tables = [
    "student",
    "course",
    "dues_v2",
    "gate_pass_log",
    "hostel_allotment",
    "chc_request",
    "chc_work_centre",
    "infra_booking",
    "transport_management_v2_route"
]
found_tables = [t for t in schema_tables if t in html]
if len(found_tables) < len(schema_tables):
    missing_tables = [t for t in schema_tables if t not in found_tables]
    print(f"[11] Schema Grounding: FAIL (missing table references: {missing_tables})")
    failures.append(f"Missing schema tables: {missing_tables}")
else:
    print(f"[11] Schema Grounding: PASS ({len(found_tables)}/{len(schema_tables)} core CollPoll production tables confirmed)")

# 12. Rendered NaN / Undefined Check in Raw HTML Elements
nan_tags = re.findall(r'>\s*(?:NaN|undefined)\s*<', html)
if nan_tags:
    print(f"[12] Static Text Integrity: FAIL (found unrendered values: {nan_tags})")
    failures.append(f"Static NaN/undefined text tags: {nan_tags}")
else:
    print("[12] Static Text Integrity: PASS (0 occurrences of static NaN or undefined text nodes)")

# 13. Server Status Check (Single Python Server Port 8000)
server_status = "Server offline on 127.0.0.1:8000 (start via 'python backend/app.py 8000')"
try:
    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/health")
    with urllib.request.urlopen(req, timeout=1.5) as resp:
        if resp.status == 200:
            server_status = "Server online on 127.0.0.1:8000 (HTTP 200 OK)"
except Exception:
    pass
print(f"[13] Server Status: {server_status}")

print("=" * 80)
if failures:
    print(f"AUDIT RESULT: FAIL ({len(failures)} issues detected)")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("AUDIT RESULT: PASS")
    sys.exit(0)
