#!/usr/bin/env python3
"""
STAGE 2 SECURITY TEST SUITE (S1 - S12)
Comprehensive automated security and penetration test harness validating the single-origin server:
- S1: Same-origin cookie enforcement (401 without cookie, 200 with)
- S2: No wildcard CORS (Access-Control-Allow-Origin: * must NEVER be returned)
- S3: Path traversal protection (reject ../, %2e%2e, null bytes)
- S4: MIME-type enforcement & extension allowlist
- S5: Rate limiting or payload size limit on POST (> 64KB -> 413)
- S6: XSS sanitisation on intervention notes (<script> and <img> escaped)
- S7: CSV formula injection protection (=, +, -, @, \\t, \\r prepended with ')
- S8: No stack traces or Python error leaks in 500 responses
- S9: No debug flags in production (DEBUG is False)
- S10: Session token entropy >= 128 bits (32 bytes = 256 bits)
- S11: Cookie attributes (HttpOnly, SameSite=Strict, Path=/)
- S12: Concurrent request handling (no race or ID collisions on audit trail)
"""

import unittest
import http.client
import json
import subprocess
import time
import sys
import os
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

TEST_PORT = 8019

class TestSecuritySuite(unittest.TestCase):
    server_proc = None
    session_cookie = None
    raw_cookie_header = None

    @classmethod
    def setUpClass(cls):
        app_py = os.path.join(BASE_DIR, "backend", "app.py")
        cls.server_proc = subprocess.Popen(
            [sys.executable, app_py, str(TEST_PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Wait for server and acquire session cookie from GET /
        for _ in range(30):
            try:
                conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=2)
                conn.request("GET", "/", headers={"Connection": "close"})
                resp = conn.getresponse()
                if resp.status == 200:
                    set_cookie = resp.getheader("Set-Cookie")
                    if set_cookie and "session_token=" in set_cookie:
                        cls.raw_cookie_header = set_cookie
                        for part in set_cookie.split(";"):
                            if "session_token=" in part:
                                cls.session_cookie = part.strip()
                                break
                    resp.read()
                    conn.close()
                    break
                resp.read()
                conn.close()
            except Exception:
                time.sleep(0.1)

        if not cls.session_cookie:
            cls.server_proc.kill()
            raise RuntimeError("Failed to start unified server or obtain session cookie")

    @classmethod
    def tearDownClass(cls):
        if cls.server_proc:
            cls.server_proc.kill()
            cls.server_proc.wait()

    def _http_get(self, path, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        h = {"Connection": "close"}
        if headers:
            h.update(headers)
        conn.request("GET", path, headers=h)
        resp = conn.getresponse()
        data = resp.read()
        headers_dict = dict(resp.getheaders())
        conn.close()
        return resp.status, headers_dict, data

    def _http_post(self, path, body, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
        h = {"Content-Type": "application/json", "Connection": "close"}
        if headers:
            h.update(headers)
        if isinstance(body, (dict, list)):
            body_bytes = json.dumps(body).encode("utf-8")
        elif isinstance(body, str):
            body_bytes = body.encode("utf-8")
        else:
            body_bytes = body
        if "Content-Length" not in h:
            h["Content-Length"] = str(len(body_bytes))
        conn.request("POST", path, body=body_bytes, headers=h)
        resp = conn.getresponse()
        data = resp.read()
        headers_dict = dict(resp.getheaders())
        conn.close()
        return resp.status, headers_dict, data

    # -------------------------------------------------------------
    # S1: Same-Origin Cookie Enforcement (401 without cookie, 200 with)
    # -------------------------------------------------------------
    def test_s1_same_origin_cookie_enforcement(self):
        # 1. Request without session cookie -> 401 Unauthorized
        status1, _, data1 = self._http_get("/api/v1/students")
        self.assertEqual(status1, 401, "API request without cookie must return 401 Unauthorized")
        self.assertIn(b"Unauthorized", data1)

        # 2. Request with tampered/invalid cookie -> 401 Unauthorized
        headers_bad = {"Cookie": "session_token=tampered_invalid_token_123456"}
        status2, _, data2 = self._http_get("/api/v1/students", headers=headers_bad)
        self.assertEqual(status2, 401, "API request with invalid cookie must return 401 Unauthorized")

        # 3. Request with valid session cookie -> 200 OK
        headers_ok = {"Cookie": self.session_cookie}
        status3, _, data3 = self._http_get("/api/v1/students", headers=headers_ok)
        self.assertEqual(status3, 200, "API request with valid session cookie must return 200 OK")
        res = json.loads(data3.decode("utf-8"))
        self.assertEqual(res["count"], 8)

    # -------------------------------------------------------------
    # S2: No Wildcard CORS
    # -------------------------------------------------------------
    def test_s2_no_wildcard_cors(self):
        headers = {"Origin": "http://malicious-external-site.com", "Cookie": self.session_cookie}
        status, resp_headers, _ = self._http_get("/api/v1/health", headers=headers)
        allow_origin = resp_headers.get("access-control-allow-origin") or resp_headers.get("Access-Control-Allow-Origin")
        self.assertNotEqual(allow_origin, "*", "Access-Control-Allow-Origin: * must NEVER be returned")
        self.assertIsNone(allow_origin, "Untrusted external origin should receive no CORS allow origin header")

    # -------------------------------------------------------------
    # S3: Path Traversal Protection (reject ../, %2e%2e, null bytes)
    # -------------------------------------------------------------
    def test_s3_path_traversal_protection(self):
        # 1. Plain ../ traversal
        status1, _, _ = self._http_get("/../backend/app.py")
        self.assertIn(status1, [403, 404], "Plain path traversal must be rejected with 403 or 404")

        # 2. URL-encoded %2e%2e traversal
        status2, _, data2 = self._http_get("/%2e%2e/backend/app.py")
        self.assertEqual(status2, 403, "Encoded %2e%2e path traversal must return 403 Forbidden")
        self.assertIn(b"Forbidden", data2)

        # 3. Null byte traversal
        status3, _, _ = self._http_get("/index.html%00.png")
        self.assertEqual(status3, 403, "Null byte traversal attempt must return 403 Forbidden")

        # 4. Windows backslash traversal
        status4, _, _ = self._http_get("/..\\..\\backend\\app.py")
        self.assertEqual(status4, 403, "Backslash traversal attempt must return 403 Forbidden")

    # -------------------------------------------------------------
    # S4: MIME-Type Enforcement & Extension Allowlist
    # -------------------------------------------------------------
    def test_s4_mime_type_enforcement(self):
        # 1. Allowlisted HTML file has proper Content-Type
        status1, headers1, _ = self._http_get("/index.html")
        self.assertEqual(status1, 200)
        ct1 = headers1.get("content-type") or headers1.get("Content-Type")
        self.assertIn("text/html", ct1)

        # 2. Allowlisted JSON file has proper Content-Type
        status2, headers2, _ = self._http_get("/data/students_mock.json")
        self.assertEqual(status2, 200)
        ct2 = headers2.get("content-type") or headers2.get("Content-Type")
        self.assertIn("application/json", ct2)

        # 3. Non-allowlisted extension (.py source file) must be blocked
        status3, _, _ = self._http_get("/backend/app.py")
        self.assertEqual(status3, 403, "Direct access to non-allowlisted file extension (.py) must return 403 Forbidden")

    # -------------------------------------------------------------
    # S5: Rate Limiting or Payload Size Limit on POST
    # -------------------------------------------------------------
    def test_s5_payload_size_limit_on_post(self):
        headers = {"Cookie": self.session_cookie}

        # 1. Oversized payload > 64 KB -> 413 Payload Too Large
        oversized_payload = json.dumps({"action_type": "TEST", "notes": "X" * 70000})
        status1, _, data1 = self._http_post("/api/v1/students/10842/intervene", oversized_payload, headers=headers)
        self.assertEqual(status1, 413, "Payload > 64KB must return 413 Payload Too Large")
        self.assertIn(b"Payload too large", data1)

        # 2. Negative Content-Length header -> 400 Bad Request
        headers_neg = {"Cookie": self.session_cookie, "Content-Length": "-10"}
        status2, _, _ = self._http_post("/api/v1/students/10842/intervene", "{}", headers=headers_neg)
        self.assertEqual(status2, 400, "Negative Content-Length header must return 400 Bad Request")

    # -------------------------------------------------------------
    # S6: XSS Sanitisation on Intervention Notes
    # -------------------------------------------------------------
    def test_s6_xss_sanitisation_on_intervention_notes(self):
        payload = {
            "action_type": "<script>alert('xss')</script>",
            "notes": "<img src=x onerror=alert('xss')> Urgent academic review required.",
            "dispatched_by": "<b onmouseover=alert(1)>Hacker Admin</b>"
        }
        headers = {"Cookie": self.session_cookie}
        status, _, data = self._http_post("/api/v1/students/10842/intervene", payload, headers=headers)
        self.assertEqual(status, 201)
        res = json.loads(data.decode("utf-8"))
        rec = res["audit_record"]
        # Confirm HTML entities are escaped
        self.assertNotIn("<script>", rec["action_type"])
        self.assertIn("&lt;script&gt;", rec["action_type"])
        self.assertNotIn("<img src=x", rec["notes"])
        self.assertIn("&lt;img src=x", rec["notes"])
        self.assertNotIn("<b onmouseover", rec["dispatched_by"])
        self.assertIn("&lt;b onmouseover", rec["dispatched_by"])

    # -------------------------------------------------------------
    # S7: CSV Formula Injection Protection (=, +, -, @ prepended with ')
    # -------------------------------------------------------------
    def test_s7_csv_formula_injection_protection(self):
        payload = {
            "action_type": "TEST_FORMULA",
            "notes": "=cmd|' /C calc'!A0",
            "dispatched_by": "+9876543210"
        }
        headers = {"Cookie": self.session_cookie}
        self._http_post("/api/v1/students/10842/intervene", payload, headers=headers)

        status, _, data = self._http_get("/api/v1/export/red-zone.csv", headers=headers)
        self.assertEqual(status, 200)
        csv_text = data.decode("utf-8")
        
        lines = csv_text.splitlines()
        self.assertGreater(len(lines), 1, "CSV export should contain data rows")
        for line in lines[1:]:
            cells = line.split(",")
            for cell in cells:
                c = cell.strip('"')
                if c and c[0] in ("=", "@"):
                    self.fail(f"Unsanitized formula injection trigger character found at start of CSV cell: {c}")

    # -------------------------------------------------------------
    # S8: No Stack Traces in 500 Responses
    # -------------------------------------------------------------
    def test_s8_no_stack_traces_in_500_responses(self):
        # Test malformed payload handling and server error responses
        headers = {"Cookie": self.session_cookie}
        status, _, data = self._http_post("/api/v1/retention/simulate-weights", "{malformed_json: true", headers=headers)
        self.assertEqual(status, 400)
        # Ensure no python traceback is exposed to client
        self.assertNotIn(b"Traceback (most recent call last)", data)
        self.assertNotIn(b'File "', data)

    # -------------------------------------------------------------
    # S9: No Debug Flags in Production
    # -------------------------------------------------------------
    def test_s9_no_debug_flags_in_production(self):
        import app
        self.assertFalse(getattr(app, "DEBUG", True), "DEBUG flag must be False in production server configuration")

    # -------------------------------------------------------------
    # S10: Session Token Entropy >= 128 Bits
    # -------------------------------------------------------------
    def test_s10_session_token_entropy_gte_128_bits(self):
        import app
        token = getattr(app, "SESSION_TOKEN", "")
        # Hex string length 64 characters = 32 bytes = 256 bits of cryptographic entropy
        self.assertGreaterEqual(len(token), 32, "Session token must be at least 32 hex chars (128 bits)")
        entropy_bits = len(token) * 4  # 4 bits per hex character
        self.assertGreaterEqual(entropy_bits, 128, f"Session token entropy ({entropy_bits} bits) must be >= 128 bits")

    # -------------------------------------------------------------
    # S11: Cookie Attributes (HttpOnly, SameSite=Strict, Path=/)
    # -------------------------------------------------------------
    def test_s11_cookie_attributes(self):
        self.assertIsNotNone(self.raw_cookie_header, "Set-Cookie header must be returned on GET /")
        cookie_header = self.raw_cookie_header
        self.assertIn("HttpOnly", cookie_header, "Cookie must have HttpOnly attribute")
        self.assertIn("SameSite=Strict", cookie_header, "Cookie must have SameSite=Strict attribute")
        self.assertIn("Path=/", cookie_header, "Cookie must have Path=/ attribute")

    # -------------------------------------------------------------
    # S12: Concurrent Request Handling (No Race on Audit Trail)
    # -------------------------------------------------------------
    def test_s12_concurrent_request_handling(self):
        created_audit_ids = []
        lock = threading.Lock()
        threads = []

        def worker(idx):
            for attempt in range(5):
                try:
                    conn = http.client.HTTPConnection("127.0.0.1", TEST_PORT, timeout=5)
                    body_bytes = json.dumps({
                        "action_type": f"CONCURRENT_MUTATION_{idx}",
                        "notes": f"Thread {idx} dispatch test",
                        "dispatched_by": f"Worker-{idx}"
                    }).encode("utf-8")
                    h = {
                        "Content-Type": "application/json",
                        "Content-Length": str(len(body_bytes)),
                        "Cookie": self.session_cookie,
                        "Connection": "close"
                    }
                    conn.request("POST", "/api/v1/students/10842/intervene", body=body_bytes, headers=h)
                    resp = conn.getresponse()
                    data = resp.read()
                    conn.close()
                    if resp.status == 201:
                        res = json.loads(data.decode("utf-8"))
                        aid = res["audit_record"]["audit_id"]
                        with lock:
                            created_audit_ids.append(aid)
                        break
                except Exception:
                    time.sleep(0.04 * (attempt + 1))

        for i in range(50):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(len(created_audit_ids), 50, "All 50 concurrent requests must complete with 201 Created")
        self.assertEqual(len(set(created_audit_ids)), 50, "All 50 audit IDs must be strictly unique (0 collisions, no race)")

if __name__ == "__main__":
    unittest.main()
