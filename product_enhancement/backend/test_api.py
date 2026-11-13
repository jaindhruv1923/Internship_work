#!/usr/bin/env python3
"""
Test Suite for Digii Campus Proactive Retention API (Real HTTP Integration Tests)
Exercises all REST endpoints over real loopback network sockets with live session cookie authentication.
"""

import unittest
import json
import os
import sys
import threading
import time
import socket
import urllib.request
import urllib.error
import http.cookiejar

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from app import DigiiCampusServer, DigiiCampusUnifiedHandler, load_initial_data, APP_STATE
from risk_engine import calculate_student_risk, DEFAULT_WEIGHTS, DEFAULT_THRESHOLDS

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

class TestDigiiCampusAPIRealHTTP(unittest.TestCase):
    server = None
    server_thread = None
    port = None
    base_url = None
    cookie_header = None
    session_token = None

    @classmethod
    def setUpClass(cls):
        load_initial_data()
        cls.port = find_free_port()
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        # Initialize and start unified server on real socket
        server_address = ("127.0.0.1", cls.port)
        cls.server = DigiiCampusServer(server_address, DigiiCampusUnifiedHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

        # Give server a moment to start
        time.sleep(0.1)

        # Acquire session cookie via initial GET /
        req = urllib.request.Request(f"{cls.base_url}/")
        with urllib.request.urlopen(req) as resp:
            set_cookie = resp.headers.get("Set-Cookie", "")
            for part in set_cookie.split(";"):
                if "session_token=" in part:
                    cls.session_token = part.strip().split("session_token=")[1]
            cls.cookie_header = f"session_token={cls.session_token}"

    @classmethod
    def tearDownClass(cls):
        if cls.server:
            cls.server.shutdown()
            cls.server.server_close()
        if cls.server_thread:
            cls.server_thread.join(timeout=1.0)

    def _http_request(self, method, path, data=None, headers=None):
        url = f"{self.base_url}{path}"
        all_headers = {"Cookie": self.cookie_header}
        if headers:
            all_headers.update(headers)
        
        body_bytes = None
        if data is not None:
            if isinstance(data, dict):
                body_bytes = json.dumps(data).encode("utf-8")
                all_headers["Content-Type"] = "application/json"
            elif isinstance(data, (str, bytes)):
                body_bytes = data.encode("utf-8") if isinstance(data, str) else data
            all_headers["Content-Length"] = str(len(body_bytes))

        req = urllib.request.Request(url, data=body_bytes, headers=all_headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                status = resp.status
                resp_headers = resp.headers
                content = resp.read()
                return status, resp_headers, content
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read()

    def test_01_session_cookie_acquired(self):
        self.assertIsNotNone(self.session_token, "Session token cookie must be acquired from GET /")
        self.assertGreater(len(self.session_token), 16, "Session token must have sufficient entropy")

    def test_02_health_endpoint(self):
        status, headers, body = self._http_request("GET", "/api/v1/health")
        self.assertEqual(status, 200)
        data = json.loads(body.decode("utf-8"))
        self.assertEqual(data.get("status").upper(), "HEALTHY")
        self.assertEqual(data.get("version"), "2.0.0")
        self.assertIn("service", data)
        self.assertEqual(data.get("students_loaded"), 8)

    def test_03_students_list_and_scores(self):
        status, headers, body = self._http_request("GET", "/api/v1/students")
        self.assertEqual(status, 200)
        data = json.loads(body.decode("utf-8"))
        self.assertIn("students", data)
        self.assertEqual(data.get("count"), 8)
        self.assertEqual(len(data["students"]), 8)

        # Check Aarav Sharma canonical score (87 HIGH)
        aarav = next((s for s in data["students"] if s["ukid"] == 10842), None)
        self.assertIsNotNone(aarav, "Aarav Sharma must exist")
        self.assertEqual(aarav["risk_profile"]["score"], 87)
        self.assertEqual(aarav["risk_profile"]["tier"], "HIGH")

        # Check Priya Nair canonical score (70 MEDIUM)
        priya = next((s for s in data["students"] if s["ukid"] == 11205), None)
        self.assertIsNotNone(priya, "Priya Nair must exist")
        self.assertEqual(priya["risk_profile"]["score"], 70)
        self.assertEqual(priya["risk_profile"]["tier"], "MEDIUM")

    def test_04_student_detail_and_404(self):
        # Valid student
        status, headers, body = self._http_request("GET", "/api/v1/students/10842")
        self.assertEqual(status, 200)
        student = json.loads(body.decode("utf-8"))
        self.assertEqual(student.get("ukid"), 10842)
        self.assertEqual(student.get("first_name"), "Aarav")

        # Invalid student
        status, headers, body = self._http_request("GET", "/api/v1/students/999999")
        self.assertEqual(status, 404)
        err = json.loads(body.decode("utf-8"))
        self.assertIn("error", err)

    def test_05_cohort_summary_analytics(self):
        status, headers, body = self._http_request("GET", "/api/v1/analytics/cohort-summary")
        self.assertEqual(status, 200)
        summary = json.loads(body.decode("utf-8"))
        self.assertEqual(summary.get("total_active_students"), 8)
        self.assertEqual(summary.get("red_zone_count"), 1)
        self.assertEqual(summary.get("amber_zone_count"), 2)
        self.assertEqual(summary.get("healthy_count"), 5)
        self.assertIn("macro_projection_illustrative", summary)
        macro = summary["macro_projection_illustrative"]
        self.assertEqual(macro.get("label"), "illustrative assumption")
        self.assertIn("projected_revenue_at_risk_formatted", macro)

    def test_06_export_red_zone_csv(self):
        status, headers, body = self._http_request("GET", "/api/v1/export/red-zone.csv")
        self.assertEqual(status, 200)
        content_type = headers.get("Content-Type", "")
        self.assertIn("text/csv", content_type)
        csv_text = body.decode("utf-8")
        lines = csv_text.strip().splitlines()
        self.assertGreater(len(lines), 1, "CSV must have header + data rows")
        header = lines[0].split(",")
        self.assertIn("UKID", header)
        self.assertIn("Enrollment_No", header)
        self.assertIn("Risk_Score", header)
        # Verify Aarav Sharma is in the red-zone CSV
        self.assertTrue(any("10842" in line and "Aarav Sharma" in line for line in lines[1:]))

    def test_07_action_intervention_dispatch(self):
        payload = {
            "action_type": "ACADEMIC_COUNSELING",
            "notes": "Discussed attendance deficit and remedial assignments.",
            "dispatched_by": "Dhruv Jain (Product Intern)"
        }
        status, headers, body = self._http_request("POST", "/api/v1/students/10842/intervene", data=payload)
        self.assertEqual(status, 201)
        resp = json.loads(body.decode("utf-8"))
        self.assertEqual(resp.get("status"), "SUCCESS")
        record = resp.get("audit_record", {})
        self.assertTrue(record.get("audit_id", "").startswith("AUD-"))
        self.assertEqual(record.get("ukid"), 10842)
        self.assertEqual(record.get("action_type"), "ACADEMIC_COUNSELING")

    def test_08_dpdp_guardian_consent_gating(self):
        payload = {
            "action_type": "GUARDIAN_ESCALATION",
            "notes": "Official notification of academic default sent to guardian with consent verified.",
            "consent_certified": True,
            "dispatched_by": "Dhruv Jain (Product Intern)"
        }
        status, headers, body = self._http_request("POST", "/api/v1/students/10842/intervene", data=payload)
        self.assertEqual(status, 201)
        resp = json.loads(body.decode("utf-8"))
        record = resp.get("audit_record", {})
        self.assertTrue(record.get("legal_review_flagged"), "Guardian intervention on adult students must flag legal review under DPDP Act")
        self.assertTrue(record.get("consent_certified"))
        self.assertTrue(record.get("delivery_metadata", {}).get("dpdp_act_2023_aligned"))

    def test_09_simulate_weights_endpoint(self):
        # 1. Valid custom weights
        custom_weights = {"academics": 0.40, "fees": 0.30, "gates": 0.10, "hostel": 0.10, "chc": 0.10}
        payload = {"weights": custom_weights}
        status, headers, body = self._http_request("POST", "/api/v1/retention/simulate-weights", data=payload)
        self.assertEqual(status, 200)
        resp = json.loads(body.decode("utf-8"))
        self.assertEqual(resp.get("status"), "RECALCULATED")
        self.assertIn("students", resp)
        self.assertEqual(len(resp["students"]), 8)

        # 2. Weights normalization: all 1.0 -> should normalize to 0.2 each
        payload_all_ones = {"weights": {"academics": 1.0, "fees": 1.0, "gates": 1.0, "hostel": 1.0, "chc": 1.0}}
        status, headers, body = self._http_request("POST", "/api/v1/retention/simulate-weights", data=payload_all_ones)
        self.assertEqual(status, 200)
        resp_ones = json.loads(body.decode("utf-8"))
        norm_weights = resp_ones.get("weights_used", {})
        for k, v in norm_weights.items():
            self.assertAlmostEqual(v, 0.2, places=3)
        for s in resp_ones["students"]:
            self.assertLessEqual(s["risk_profile"]["score"], 100)

        # 3. Invalid weights (string type) -> 400
        payload_bad_type = {"weights": {"academics": "invalid_weight"}}
        status, headers, body = self._http_request("POST", "/api/v1/retention/simulate-weights", data=payload_bad_type)
        self.assertEqual(status, 400)

        # 4. Inverted thresholds (amber >= red) -> 400
        payload_inverted = {"thresholds": {"red_zone": 30, "amber_zone": 80}}
        status, headers, body = self._http_request("POST", "/api/v1/retention/simulate-weights", data=payload_inverted)
        self.assertEqual(status, 400)

    def test_10_b2b2c_action_dispatch(self):
        # Valid B2B2C action
        payload = {"action": "SIMULATE_NO_DUES_CLEARANCE", "ukid": 10842}
        status, headers, body = self._http_request("POST", "/api/v1/b2b2c/action", data=payload)
        self.assertEqual(status, 200)
        resp = json.loads(body.decode("utf-8"))
        self.assertEqual(resp.get("status"), "SUCCESS")
        self.assertEqual(resp.get("action"), "SIMULATE_NO_DUES_CLEARANCE")

        # Invalid action (unapproved / malicious) -> 400
        payload_invalid = {"action": "LAUNCH_NUKES", "ukid": 10842}
        status, headers, body = self._http_request("POST", "/api/v1/b2b2c/action", data=payload_invalid)
        self.assertEqual(status, 400)

        # Non-existent student ukid -> 404
        payload_bad_ukid = {"action": "SIMULATE_NO_DUES_CLEARANCE", "ukid": 999999}
        status, headers, body = self._http_request("POST", "/api/v1/b2b2c/action", data=payload_bad_ukid)
        self.assertEqual(status, 404)

    def test_11_audit_trail_retrieval(self):
        status, headers, body = self._http_request("GET", "/api/v1/audit/trail")
        self.assertEqual(status, 200)
        resp = json.loads(body.decode("utf-8"))
        self.assertIn("audit_trail", resp)
        self.assertGreater(len(resp["audit_trail"]), 0, "Audit trail should have recorded actions from test_07 and test_08")

    def test_12_scoring_parity_with_risk_engine(self):
        status, headers, body = self._http_request("GET", "/api/v1/students")
        self.assertEqual(status, 200)
        students = json.loads(body.decode("utf-8"))["students"]
        for s in students:
            canonical = calculate_student_risk(s, DEFAULT_WEIGHTS, DEFAULT_THRESHOLDS)
            self.assertEqual(s["risk_profile"]["score"], canonical["score"], f"Score mismatch for UKID {s['ukid']}")
            self.assertEqual(s["risk_profile"]["tier"], canonical["tier"], f"Tier mismatch for UKID {s['ukid']}")

    def test_13_demo_reset_endpoint(self):
        status, headers, body = self._http_request("POST", "/api/v1/demo/reset")
        self.assertEqual(status, 200)
        resp = json.loads(body.decode("utf-8"))
        self.assertEqual(resp.get("status"), "RESET")
        self.assertEqual(resp.get("total_students"), 8)
        self.assertEqual(resp.get("audit_entries"), 0)

if __name__ == "__main__":
    unittest.main()
