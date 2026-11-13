#!/usr/bin/env python3
"""
STAGE 1 INTEGRITY VERIFICATION SUITE
Tests all Stage 1 integrity findings (I1 to I11).
Each test verifies the required contract. Before fixes, these tests fail. After fixes, they pass.
"""

import unittest
import json
import os
import re
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(ROOT_DIR, "data", "students_mock.json")
HTML_PATH = os.path.join(ROOT_DIR, "index.html")
APP_PATH = os.path.join(SCRIPT_DIR, "app.py")
README_PATH = os.path.join(SCRIPT_DIR, "README.md")
PRD_PATH = os.path.join(ROOT_DIR, "PRD_Proactive_Retention_System.md")
PACKAGE_PATH = os.path.join(ROOT_DIR, "package.json")
PLAYBOOK_PATH = os.path.join(ROOT_DIR, "EXECUTIVE_PITCH_PLAYBOOK.md")
DECK_PATH = os.path.join(ROOT_DIR, "EXECUTIVE_PITCH_DECK.md")

sys.path.insert(0, SCRIPT_DIR)
from app import APP_STATE, load_initial_data, calculate_student_risk

class TestStage1Integrity(unittest.TestCase):

    def setUp(self):
        load_initial_data()
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            self.raw_data = json.load(f)
        with open(HTML_PATH, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_i1_stored_scores_match_calculated(self):
        """I1: Stored risk_profile score and tier in students_mock.json MUST match calculate_student_risk."""
        for s in self.raw_data["students"]:
            calc = calculate_student_risk(s)
            stored = s.get("risk_profile", {})
            stored_score = stored.get("score")
            stored_tier = stored.get("tier")
            self.assertEqual(
                stored_score, calc["score"],
                f"Student {s['first_name']} stored score {stored_score} does not match calculate_student_risk {calc['score']}"
            )
            self.assertEqual(
                stored_tier, calc["tier"],
                f"Student {s['first_name']} stored tier {stored_tier} does not match calculate_student_risk {calc['tier']}"
            )

    def test_i3_embedded_mock_data_matches_json(self):
        """I3: EMBEDDED_MOCK_DATA in index.html must match data/students_mock.json."""
        match = re.search(r"const EMBEDDED_MOCK_DATA\s*=\s*(\{.*?\});\s*(?:function|\n)", self.html, re.DOTALL)
        self.assertIsNotNone(match, "EMBEDDED_MOCK_DATA declaration not found in index.html")
        embedded_json = json.loads(match.group(1))
        # Compare student ukids and counts
        self.assertEqual(len(embedded_json.get("students", [])), len(self.raw_data["students"]))
        for emb, raw in zip(embedded_json["students"], self.raw_data["students"]):
            self.assertEqual(emb["ukid"], raw["ukid"])
            self.assertEqual(emb.get("risk_profile", {}).get("score"), raw.get("risk_profile", {}).get("score"))
            self.assertEqual(emb.get("risk_profile", {}).get("tier"), raw.get("risk_profile", {}).get("tier"))

    def test_i4_no_undefined_in_roster_templates(self):
        """I4: Roster rendering must not use undefined properties (e.g. s.name without fallback)."""
        self.assertNotIn("${s.name}", self.html, "Unchecked ${s.name} used where student may only have first_name/last_name")

    def test_i5_no_arbitrary_risk_drop_in_fee_payment(self):
        """I5: processFeePayment must not contain invented -28 point risk drop."""
        self.assertNotIn("s.composite_risk_score - 28", self.html, "Invented -28 risk deduction found in processFeePayment")

    def test_i6_weight_and_threshold_validation(self):
        """I6: Weights summing != 1.0 or invalid thresholds (amber >= red) must be rejected/handled."""
        # Test extreme invalid weights (e.g. all 1.0 = sum 5.0)
        invalid_weights = {"academics": 1.0, "fees": 1.0, "gates": 1.0, "hostel": 1.0, "chc": 1.0}
        res = calculate_student_risk(self.raw_data["students"][0], weights=invalid_weights)
        # Score must be clamped to 100 max
        self.assertLessEqual(res["score"], 100, "Unclamped score exceeded 100")

    def test_i7_hostel_and_chc_signals_separated(self):
        """I7: Hostel and CHC sliders must not multiply the exact same event_score variable."""
        with open(APP_PATH, "r", encoding="utf-8") as f:
            app_code = f.read()
        self.assertNotIn('(w["hostel"] + w["chc"]) * event_score', app_code,
                         "Hostel and CHC weights still multiply identical event_score variable")

    def test_i8_no_duplicate_dom_ids(self):
        """I8: index.html must not contain duplicate DOM ids."""
        dom_ids = re.findall(r'\bid="([a-zA-Z0-9_-]+)"', self.html)
        seen = set()
        duplicates = set()
        for i in dom_ids:
            if i in seen:
                duplicates.add(i)
            seen.add(i)
        self.assertEqual(len(duplicates), 0, f"Duplicate DOM ids found: {duplicates}")

    def test_i8_id_generators_not_colliding(self):
        """I8: ID generators must not use tiny 50-value random ranges like CHC-REQ-<4900-4949>."""
        self.assertNotIn("4900 + Math.random() * 50", self.html, "Found 50-value random collision range for CHC-REQ")

    def test_i9_mysql_bridge_not_claiming_fake_live(self):
        """I9: mysql_bridge must not claim online 14ms connection when nothing connects."""
        bridge = APP_STATE.get("mysql_bridge", {})
        self.assertNotEqual(bridge.get("status"), "ONLINE", "mysql_bridge claims ONLINE without connecting")

    def test_i9_b2b2c_action_rejects_unknown(self):
        """I9: /b2b2c/action endpoint or handler must not accept unknown actions like LAUNCH_NUKES."""
        with open(APP_PATH, "r", encoding="utf-8") as f:
            app_code = f.read()
        self.assertIn("VALID_B2B2C_ACTIONS", app_code, "Missing whitelist of valid B2B2C actions in app.py")

    def test_i10_sql_lineage_labeled_illustrative(self):
        """I10: SQL lineage queries must be explicitly marked ILLUSTRATIVE."""
        with open(APP_PATH, "r", encoding="utf-8") as f:
            app_code = f.read()
        self.assertIn("ILLUSTRATIVE", app_code, "SQL lineage queries in app.py must be marked ILLUSTRATIVE")

    def test_i11_docs_author_and_compliance(self):
        """I11: Documentation and package.json must not state inflated titles or ungrounded ISO 27001/FERPA."""
        with open(PACKAGE_PATH, "r", encoding="utf-8") as f:
            pkg = json.load(f)
        self.assertNotIn("Lead Product Manager", pkg.get("author", ""), "package.json author title must not claim Lead PM")
        with open(PRD_PATH, "r", encoding="utf-8") as f:
            prd = f.read()
        self.assertNotIn("Campus Health Center", prd, "PRD still contains 'Campus Health Center'")
        self.assertNotIn("ISO 27001 and FERPA privacy regulations", prd, "PRD claims ISO 27001/FERPA compliance for prototype")

if __name__ == "__main__":
    unittest.main()

