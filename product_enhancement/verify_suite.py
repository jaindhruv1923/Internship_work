# -*- coding: utf-8 -*-
"""
COMPREHENSIVE POST-RECONSTRUCTION VERIFICATION
"""
import re
import os

HTML_PATH = r"C:\Users\Admin\Desktop\worklogs\product_enhancement\index.html"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Index HTML Size: {len(html):,} bytes ({len(html.splitlines()):,} lines)")
print("=" * 70)

# 1. SPA_VIEWS
spa_match = re.search(r"const SPA_VIEWS = \[([^\]]+)\];", html)
views = [v.strip().strip("'\"") for v in spa_match.group(1).split(",") if v.strip()]
print(f"[1] SPA_VIEWS: {len(views)} views: {views}")

# 2. HTML sections
missing_sections = [v for v in views if f'id="view-{v}"' not in html]
print(f"[2] HTML sections: {'PASS' if not missing_sections else 'FAIL: ' + str(missing_sections)}")

# 3. Nav links
missing_nav = [v for v in views if f'id="nav-{v}"' not in html]
print(f"[3] Sidebar nav: {'PASS' if not missing_nav else 'FAIL: ' + str(missing_nav)}")

# 4. Emojis
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
emojis = emoji_pattern.findall(html)
print(f"[4] Emojis: {'PASS (0)' if not emojis else f'FAIL ({len(emojis)})'}")

# 5. onclick handlers
onclick_matches = re.findall(r'onclick="([a-zA-Z0-9_]+)\(', html)
unique_handlers = sorted(set(onclick_matches))
js_func_defs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html))
missing_handlers = [h for h in unique_handlers if h not in js_func_defs]
print(f"[5] Handlers: {len(unique_handlers)} onclick, {len(missing_handlers)} missing: {'PASS' if not missing_handlers else missing_handlers}")

# 6. Tone check
tone_words = {
    "POSH": html.count("POSH"),
    "legacy (visible UI)": len([m for m in re.finditer(r'\blegacy\b', html, re.I) if 'Legacy hostel master' not in html[max(0,m.start()-40):m.end()+40] and '<!-- ' not in html[max(0,m.start()-10):m.start()]]),
    "passive record": html.lower().count("passive record"),
    "clunky": html.lower().count("clunky"),
    "siloed nightmare": html.lower().count("siloed nightmare"),
}
print(f"[6] Tone check:")
for word, count in tone_words.items():
    status = "PASS" if count == 0 else f"WARNING ({count})"
    print(f"     {word}: {status}")

# 7. CHC definition check
chc_health = html.count("Campus Health Clinic") + html.count("Campus Health Center")
chc_help = html.count("Campus Help Centre")
print(f"[7] CHC definition: 'Campus Health' refs = {chc_health} (should be 0), 'Campus Help Centre' refs = {chc_help}")

# 8. Simulated data disclaimer
has_disclaimer = "Simulated Enterprise Cohort" in html
print(f"[8] Data disclaimer: {'PASS' if has_disclaimer else 'FAIL'}")

# 9. CollPoll schema references
schema_refs = {
    "chc_middleware": html.count("chc_middleware"),
    "chc_request": html.count("chc_request"),
    "chc_work_centre": html.count("chc_work_centre"),
    "gate_pass_log": html.count("gate_pass_log"),
    "hostel_allotment": html.count("hostel_allotment"),
    "infra_booking": html.count("infra_booking"),
    "transport_management_v2": html.count("transport_management_v2"),
    "dues_v2": html.count("dues_v2"),
    "placement_application": html.count("placement_application"),
}
print(f"[9] CollPoll schema references:")
for table, count in schema_refs.items():
    print(f"     {table}: {count}")

print("=" * 70)
all_pass = (not missing_sections and not missing_nav and not emojis and not missing_handlers
            and tone_words["POSH"] == 0 and chc_health == 0 and has_disclaimer)
print(f"OVERALL: {'ALL CHECKS PASS' if all_pass else 'SOME CHECKS NEED ATTENTION'}")
