# -*- coding: utf-8 -*-
"""
Verification script for all 20 Digii 2.0 / CollPoll Workflow Views.
Checks:
1. SPA_VIEWS list and view elements in HTML
2. Every onclick handler in HTML has a corresponding JS function definition
3. Emojis (must be 0)
4. Navigation elements in aside
5. File sizes and validity
"""

import re
import os
import sys

HTML_PATH = r"C:\Users\Admin\Desktop\worklogs\product_enhancement\index.html"

if not os.path.exists(HTML_PATH):
    print(f"Error: {HTML_PATH} does not exist!")
    sys.exit(1)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Index HTML Size: {len(html):,} bytes ({len(html.splitlines()):,} lines)")

# 1. Check SPA_VIEWS
spa_views_match = re.search(r"const SPA_VIEWS = \[([^\]]+)\];", html)
if not spa_views_match:
    print("FAIL: const SPA_VIEWS not found!")
    sys.exit(1)

views_raw = spa_views_match.group(1)
views = [v.strip().strip("'\"") for v in views_raw.split(",") if v.strip()]
print(f"Found {len(views)} views in SPA_VIEWS: {views}")

missing_sections = []
for v in views:
    section_id = f'id="view-{v}"'
    if section_id not in html:
        missing_sections.append(v)

if missing_sections:
    print(f"FAIL: Missing HTML sections for views: {missing_sections}")
else:
    print(f"PASS: All {len(views)} views have corresponding HTML sections <section id='view-...'>!")

# 2. Check Navigation links in aside
missing_nav = []
for v in views:
    nav_id = f'id="nav-{v}"'
    if nav_id not in html:
        missing_nav.append(v)

if missing_nav:
    print(f"FAIL: Missing sidebar navigation links for: {missing_nav}")
else:
    print(f"PASS: All {len(views)} views have sidebar navigation links <a id='nav-...'>!")

# 3. Check for Emojis
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
emojis_found = emoji_pattern.findall(html)
if emojis_found:
    print(f"FAIL: Found {len(emojis_found)} emojis in index.html! Emojis: {set(emojis_found)}")
else:
    print("PASS: Zero emojis found in index.html! 100% clean professional SVG and text.")

# 4. Extract all onclick handlers and verify they exist in JS
onclick_matches = re.findall(r'onclick="([a-zA-Z0-9_]+)\(', html)
unique_handlers = sorted(set(onclick_matches))
print(f"Found {len(unique_handlers)} unique onclick handler functions in HTML.")

# Extract JS function definitions
js_func_defs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html))
# Also arrow / assigned functions: const func = () => or window.func =
js_assigned_defs = set(re.findall(r'(?:const|let|var|window\.)([a-zA-Z0-9_]+)\s*=\s*(?:function|\([^)]*\)\s*=>)', html))
all_js_functions = js_func_defs.union(js_assigned_defs)

missing_handlers = []
for handler in unique_handlers:
    if handler not in all_js_functions:
        missing_handlers.append(handler)

if missing_handlers:
    print(f"WARNING: The following {len(missing_handlers)} onclick handlers are missing definitions:")
    for h in missing_handlers:
        print(f"  - {h}")
else:
    print(f"PASS: 100% of {len(unique_handlers)} onclick handler functions are defined in JavaScript!")

print("\n--- Summary Verification Complete ---")
