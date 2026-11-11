#!/usr/bin/env python3
"""
Test Suite for Digii Campus Proactive Retention API
Ensures all endpoints, risk heuristics, audit trails, and data structures pass validation.
"""

import unittest
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from app import APP_STATE, load_initial_data, calculate_student_risk

class TestDigiiCampusAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_initial_data()

    def test_student_data_loaded(self):
        self.assertGreater(len(APP_STATE["students"]), 0, "Students array should not be empty")
        self.assertEqual(len(APP_STATE["students"]), 8, "Expected 8 mock student records")

    def test_high_risk_aarav_sharma(self):
        aarav = next((s for s in APP_STATE["students"] if s["ukid"] == 10842), None)
        self.assertIsNotNone(aarav, "Aarav Sharma should exist in dataset")
        self.assertEqual(aarav["risk_profile"]["tier"], "HIGH", "Aarav should be HIGH risk tier")
        self.assertGreaterEqual(aarav["risk_profile"]["score"], 75, "Aarav risk score should be >= 75")

    def test_high_risk_priya_nair(self):
        priya = next((s for s in APP_STATE["students"] if s["ukid"] == 11205), None)
        self.assertIsNotNone(priya, "Priya Nair should exist in dataset")
        self.assertEqual(priya["risk_profile"]["tier"], "HIGH", "Priya should be HIGH risk tier")

    def test_risk_recalculation_heuristics(self):
        student = APP_STATE["students"][0]
        # Test default weights
        risk_default = calculate_student_risk(student)
        self.assertIn("score", risk_default)
        self.assertIn("tier", risk_default)
        self.assertIn("sub_scores", risk_default)
        self.assertGreaterEqual(risk_default["score"], 0)
        self.assertLessEqual(risk_default["score"], 100)

        # Test extreme academic weight (100% academic)
        weights_acad = {"academics": 1.0, "fees": 0.0, "gates": 0.0, "hostel": 0.0, "chc": 0.0}
        risk_acad = calculate_student_risk(student, weights=weights_acad)
        self.assertIsInstance(risk_acad["score"], int)

    def test_schema_cross_module_keys(self):
        for s in APP_STATE["students"]:
            self.assertIn("ukid", s)
            self.assertIn("enrollment_no", s)
            self.assertIn("academics", s)
            self.assertIn("finance", s)
            self.assertIn("access_gate_telemetry", s)
            self.assertIn("timeline_events", s)

    def test_mysql_bridge_and_b2b2c_state(self):
        self.assertIn("mysql_bridge", APP_STATE)
        self.assertEqual(APP_STATE["mysql_bridge"]["database"], "collpoll")
        self.assertEqual(APP_STATE["mysql_bridge"]["table_count"], 1647)
        self.assertIn("b2b2c_features", APP_STATE)
        self.assertEqual(len(APP_STATE["b2b2c_features"]), 10)

    def test_html_onclick_handlers_integrity(self):
        import re
        html_path = os.path.join(SCRIPT_DIR, '..', 'index.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        raw_onclicks = re.findall(r'onclick=["\']([^"\']+)["\']', html)
        called_funcs = set()
        for raw in raw_onclicks:
            m = re.match(r'([a-zA-Z0-9_]+)\s*\(', raw.strip())
            if m:
                called_funcs.add(m.group(1))

        script_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
        self.assertIsNotNone(script_match, "index.html should have a script block")
        script_text = script_match.group(1)
        defined_funcs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', script_text))
        defined_funcs.update(re.findall(r'window\.([a-zA-Z0-9_]+)\s*=', script_text))
        defined_funcs.update(re.findall(r'const\s+([a-zA-Z0-9_]+)\s*=\s*\(', script_text))

        missing = [fn for fn in sorted(called_funcs) if fn not in defined_funcs and not fn.startswith('console') and not fn.startswith('alert')]
        self.assertEqual(len(missing), 0, f"Missing onclick handlers in index.html: {missing}")

if __name__ == "__main__":
    unittest.main()
