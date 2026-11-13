#!/usr/bin/env python3
"""
Digii Campus (CollPoll) — Proactive Retention & Intelligence System API
Stage 2 Unified Server & Algorithmic Heuristic Engine

Author: Dhruv Jain (Product & Data Architecture Intern)
Reporting to: Mr. Suraj Bhatt (Engineering & BI Manager) & Saksham Gupta (Principal Engineer)
Architecture: Single-Origin Thread-Safe Python 3 Server serving allowlisted UI & authenticated RESTful API
"""

import sys
import os
import json
import csv
import io
import time
import secrets
import html
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from datetime import datetime, timezone

# Resolve workspace root and mock data path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PARENT_DIR, "data", "students_mock.json")
SCHEMA_FILE = os.path.join(PARENT_DIR, "data", "schema_definition.json")
INDEX_FILE = os.path.join(PARENT_DIR, "index.html")

# Import canonical single scoring engine
sys.path.insert(0, SCRIPT_DIR)
from risk_engine import (
    calculate_student_risk,
    validate_weights,
    validate_thresholds,
    DEFAULT_WEIGHTS,
    DEFAULT_THRESHOLDS
)
import database
import analytics_engine

DEBUG = False

# Cryptographically strong per-run session token (delivered via HttpOnly SameSite=Strict cookie)
SESSION_TOKEN = secrets.token_hex(32)

# Threading Lock for safe concurrent state mutations
STATE_LOCK = threading.Lock()

# Monotonic Audit Counter (prevents collisions)
AUDIT_COUNTER = 100

# Whitelisted valid innovation actions for B2B2C concept simulations
VALID_B2B2C_ACTIONS = {
    "SIMULATE_NO_DUES_CLEARANCE",
    "BALANCE_ASSIGNMENTS",
    "GENERATE_RESUME",
    "LOG_ROOM_MAINTENANCE",
    "BOOK_OFFICE_HOURS",
    "SYNC_MEDICAL_LEAVE",
    "MATCH_ELECTIVE",
    "LIST_MARKETPLACE_ITEM",
    "ISSUE_NFC_CAMPUS_PASS",
    "REQUEST_P2P_TUTOR"
}

# Allowlisted extensions for static asset serving
ALLOWED_STATIC_EXTENSIONS = {
    ".html": "text/html; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".csv": "text/csv; charset=utf-8"
}

# In-Memory State & Audit Log
APP_STATE = {
    "students": [],
    "system_metadata": {},
    "audit_trail": [],
    "heuristic_weights": dict(DEFAULT_WEIGHTS),
    "risk_thresholds": dict(DEFAULT_THRESHOLDS),
    "mysql_bridge": {
        "service": "MySQL80 (Simulated / Stand-in)",
        "port": 3306,
        "host": "localhost",
        "database": "collpoll",
        "status": "SIMULATED_STANDIN",
        "live_connection": False,
        "note": "Illustrative stand-in; no live socket connection established",
        "table_count": 1647,
        "dump_size_gb": 10.08
    },
    "b2b2c_features": [
        {"id": 1, "title": "Zero-Friction Digital No-Dues", "status": "PROPOSED_CONCEPT", "student_win": "Zero waiting outside 10 offices", "university_win": "100% fee clearance before degrees"},
        {"id": 2, "title": "Smart Assignment Deadline Balancer", "status": "PROPOSED_CONCEPT", "student_win": "Prevents burnout on Friday overlaps", "university_win": "Higher quality project submissions"},
        {"id": 3, "title": "Verified Digital Auto-Resume Generator", "status": "PROPOSED_CONCEPT", "student_win": "Instant verified web portfolio", "university_win": "Placement cell eliminates fake CGPAs"},
        {"id": 4, "title": "Unified Geo-Tagged Maintenance Ticketing", "status": "PROPOSED_CONCEPT", "student_win": "Photo room tickets without paper registers", "university_win": "Single-trip repair cluster dispatch"},
        {"id": 5, "title": "Seamless Office Hours Booking System", "status": "PROPOSED_CONCEPT", "student_win": "Guaranteed 15-min faculty consultation", "university_win": "Protects professor deep-work hours"},
        {"id": 6, "title": "Automated Medical Leave & CHC Sync", "status": "PROPOSED_CONCEPT", "student_win": "No carrying paper slips to 6 professors", "university_win": "Zero fake medical attendance claims"},
        {"id": 7, "title": "AI-Powered Elective & Major Matchmaker", "status": "PROPOSED_CONCEPT", "student_win": "Electives matched to past grade strengths", "university_win": "Early predictive classroom capacity sizing"},
        {"id": 8, "title": "Dynamic Campus Marketplace & Lost-and-Found", "status": "PROPOSED_CONCEPT", "student_win": "Peer textbook & lab coat savings", "university_win": "Security freed from managing lost items"},
        {"id": 9, "title": "Universal NFC/QR Campus Wallet", "status": "PROPOSED_CONCEPT", "student_win": "Phone-only campus survival", "university_win": "Proxy-proof gate & mess consumption data"},
        {"id": 10, "title": "Peer-to-Peer Micro-Tutoring Network", "status": "PROPOSED_CONCEPT", "student_win": "Remedial help from peers; credits earned", "university_win": "Higher pass rates without remedial faculty load"}
    ]
}

def load_initial_data():
    """Loads student relational dataset, initializes SQLite database with WAL mode, and computes canonical scores."""
    global AUDIT_COUNTER
    with STATE_LOCK:
        try:
            # Initialize SQLite persistent schema and seed data
            database.init_database()
            db_students = database.get_students()
            db_audit = database.get_audit_trail()
            weights, thresholds = database.get_weights_and_thresholds()

            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                APP_STATE["system_metadata"] = data.get("system_metadata", {})

            APP_STATE["students"] = db_students if db_students else data.get("students", [])
            APP_STATE["audit_trail"] = db_audit if db_audit else []
            APP_STATE["heuristic_weights"] = weights if weights else dict(DEFAULT_WEIGHTS)
            APP_STATE["risk_thresholds"] = thresholds if thresholds else dict(DEFAULT_THRESHOLDS)
            AUDIT_COUNTER = 100 + len(APP_STATE["audit_trail"])
            print(f"[Backend] Successfully initialized SQLite WAL database with {len(APP_STATE['students'])} students and {len(APP_STATE['audit_trail'])} audit records")
            # Ensure risk scores strictly match the single canonical scoring engine
            for s in APP_STATE["students"]:
                calc = calculate_student_risk(s, APP_STATE["heuristic_weights"], APP_STATE["risk_thresholds"])
                s.setdefault("risk_profile", {})
                s["risk_profile"]["score"] = calc["score"]
                s["risk_profile"]["tier"] = calc["tier"]
                s["risk_profile"]["sub_scores"] = calc["sub_scores"]
                s["risk_profile"]["heuristic_risk_index"] = calc["score"]
        except Exception as e:
            print(f"[Backend Error] Failed loading {DATA_FILE}: {e}")
            APP_STATE["students"] = []

def sanitize_csv_cell(val):
    """Mitigate CSV formula injection (=, +, -, @, \\t, \\r)."""
    s = str(val) if val is not None else ""
    if s and s[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + s
    return s

class DigiiCampusUnifiedHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    close_connection = True

    def log_message(self, format, *args):
        # Suppress stderr logging to prevent OS pipe buffer deadlocks in subprocesses
        pass

    def _get_cookie_token(self):
        """Extracts session_token from Cookie header, or falls back to X-Session-Token / Bearer."""
        cookie_header = self.headers.get("Cookie", "")
        cookies = {}
        for item in cookie_header.split(";"):
            if "=" in item:
                k, v = item.strip().split("=", 1)
                cookies[k.strip()] = v.strip()
        
        token = cookies.get("session_token")
        if not token:
            token = self.headers.get("X-Session-Token")
        if not token:
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                token = auth[7:].strip()
        return token

    def _is_authenticated(self):
        """Validates the request session token against the active per-run token."""
        token = self._get_cookie_token()
        if not token:
            return False
        return secrets.compare_digest(token, SESSION_TOKEN)

    def _set_cors_headers(self):
        """Strict same-origin CORS: never wildcard '*'."""
        origin = self.headers.get("Origin")
        if origin:
            parsed_origin = urlparse(origin)
            if parsed_origin.hostname in ("127.0.0.1", "localhost"):
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Access-Control-Allow-Credentials", "true")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Session-Token")

    def _send_json(self, status_code, data):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Connection", "close")
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        raw_path = self.path
        parsed = urlparse(raw_path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # -------------------------------------------------------------
        # Security: Detect Path Traversal attempts upfront
        if "%2e" in raw_path.lower() or "%2f" in raw_path.lower() or "%00" in raw_path.lower() or "\0" in raw_path or ".." in path or "..\\" in raw_path:
            self._send_json(403, {"error": "Forbidden: Path traversal detected"})
            return

        with STATE_LOCK:
            APP_STATE.setdefault("request_log", []).append({
                "method": "GET",
                "path": path,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        # -------------------------------------------------------------
        # API Routes: /api/... (Strict Authentication Required)
        # -------------------------------------------------------------
        if path.startswith("/api/"):
            if not self._is_authenticated():
                self._send_json(401, {"error": "Unauthorized: Missing or invalid session token cookie"})
                return

            # 1. Health & Readiness
            if path == "/api/v1/health":
                with STATE_LOCK:
                    students_count = len(APP_STATE["students"])
                    audit_count = len(APP_STATE["audit_trail"])
                self._send_json(200, {
                    "status": "HEALTHY",
                    "service": "Digii Campus Proactive Retention API",
                    "version": "2.0.0",
                    "database_engine": "SQLite 3 (WAL Mode, ACID Durability)",
                    "persistence_active": True,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "students_loaded": students_count,
                    "audit_entries_logged": audit_count
                })
                return

            # 2. Cohort Summary / KPIs (Computed from 8 mock students)
            if path == "/api/v1/analytics/cohort-summary":
                with STATE_LOCK:
                    students = APP_STATE["students"]
                    total_active = len(students)
                    red_count = sum(1 for s in students if s["risk_profile"]["tier"] == "HIGH")
                    amber_count = sum(1 for s in students if s["risk_profile"]["tier"] == "MEDIUM")
                    healthy_count = sum(1 for s in students if s["risk_profile"]["tier"] == "HEALTHY")
                    revenue_risk = sum(s["finance"].get("amount_overdue", 0) for s in students if s["risk_profile"]["tier"] == "HIGH")
                    avg_health = round(sum(100 - s["risk_profile"]["score"] for s in students) / total_active, 1) if total_active > 0 else 0.0

                    resp = {
                        "total_active_students": total_active,
                        "red_zone_count": red_count,
                        "amber_zone_count": amber_count,
                        "healthy_count": healthy_count,
                        "global_institution_health_score": avg_health,
                        "revenue_at_risk_inr": revenue_risk,
                        "revenue_at_risk_formatted": f"₹{revenue_risk/100000:.2f} Lakhs",
                        "macro_projection_illustrative": {
                            "label": "illustrative assumption",
                            "formula": "Hypothetical macro model (not an empirical Digii figure): assume ~3% red (150 students) of 5,000 cohort * ₹1.30L avg overdue = ₹1.95 Cr; +14% funnel lift = ₹55 Lakhs",
                            "projected_students": 5000,
                            "projected_red_zone": 150,
                            "projected_amber_zone": 400,
                            "projected_healthy": 4450,
                            "projected_revenue_at_risk_formatted": "₹1.95 Cr",
                            "projected_recovered_tuition_formatted": "₹55 Lakhs"
                        },
                        "weights_active": APP_STATE["heuristic_weights"],
                        "thresholds_active": APP_STATE["risk_thresholds"]
                    }
                self._send_json(200, resp)
                return

            # 3. Students List
            if path == "/api/v1/students":
                tier_filter = query.get("tier", [None])[0]
                dept_filter = query.get("dept", [None])[0]
                search_query = query.get("q", [None])[0]

                with STATE_LOCK:
                    filtered = list(APP_STATE["students"])

                if tier_filter and tier_filter.upper() != "ALL":
                    filtered = [s for s in filtered if s["risk_profile"]["tier"] == tier_filter.upper()]
                if dept_filter and dept_filter.upper() != "ALL":
                    filtered = [s for s in filtered if s["department"].upper() == dept_filter.upper()]
                if search_query:
                    sq = search_query.lower()
                    filtered = [s for s in filtered if sq in s["first_name"].lower() or sq in s["last_name"].lower() or sq in s["enrollment_no"].lower()]

                self._send_json(200, {"count": len(filtered), "students": filtered})
                return

            # 4. Student Detail by UKID: /api/v1/students/{ukid}
            if path.startswith("/api/v1/students/"):
                parts = path.strip("/").split("/")
                if len(parts) == 4 and parts[3].isdigit():
                    ukid = int(parts[3])
                    with STATE_LOCK:
                        student = next((s for s in APP_STATE["students"] if s["ukid"] == ukid), None)
                    if student:
                        self._send_json(200, student)
                    else:
                        self._send_json(404, {"error": f"Student UKID {ukid} not found"})
                    return

            # 5. Audit Trail History
            if path == "/api/v1/audit/trail":
                ukid_filter = query.get("ukid", [None])[0]
                with STATE_LOCK:
                    logs = list(APP_STATE["audit_trail"])
                if ukid_filter and ukid_filter.isdigit():
                    logs = [l for l in logs if l.get("ukid") == int(ukid_filter)]
                self._send_json(200, {"count": len(logs), "audit_trail": logs})
                return

            # 6. SQL Lineage Repository Endpoint
            if path == "/api/v1/sql/lineage":
                sql_queries = {
                    "kpi_aggregation": """
SELECT
    COUNT(DISTINCT u.ukid) AS total_cohort,
    COUNT(DISTINCT CASE WHEN crs.composite_score >= 75 THEN u.ukid END) AS red_zone_count,
    COUNT(DISTINCT CASE WHEN crs.composite_score BETWEEN 50 AND 74 THEN u.ukid END) AS amber_zone_count,
    SUM(CASE WHEN crs.composite_score >= 75 THEN dv.amount_overdue ELSE 0 END) AS revenue_at_risk_inr
FROM student u
INNER JOIN collpoll_composite_retention_scores crs ON u.ukid = crs.ukid /* [ASSUMED] */
LEFT JOIN dues_v2 dv ON u.ukid = dv.student_ukid /* [ASSUMED join key] */ AND dv.status = 'OVERDUE';
                    """.strip(),
                    "student_360_chronological": """
SELECT
    'ACADEMICS' AS module,
    ca.attendance_date AS event_timestamp, /* [ASSUMED column] */
    'Absence Warning' AS title,
    CONCAT('Absent in ', c.course_name) AS description, /* [ASSUMED column] */
    'CRITICAL' AS severity
FROM classroom_attendance ca
JOIN course c ON ca.course_id = c.id /* [ASSUMED join] */
WHERE ca.student_ukid = 10842 AND ca.status = 'ABSENT' /* [ASSUMED status] */

UNION ALL

SELECT
    'FINANCE' AS module,
    dv.due_date AS event_timestamp, /* [ASSUMED column] */
    'Tuition Fee Default Notice' AS title,
    CONCAT('Installment overdue. Amount: ₹', dv.amount_overdue) AS description,
    'WARNING' AS severity
FROM dues_v2 dv
WHERE dv.student_ukid = 10842 AND dv.status = 'OVERDUE' /* [ASSUMED column] */

UNION ALL

SELECT
    'ACCESS_GATE' AS module,
    gpl.punch_timestamp AS event_timestamp,
    'Curfew Breach Logged' AS title,
    'Late return past campus curfew' AS description,
    'CRITICAL' AS severity
FROM gate_pass_log gpl
WHERE gpl.student_ukid = 10842 AND gpl.status_id = 3 /* [ASSUMED curfew status] */
ORDER BY event_timestamp DESC
LIMIT 25;
                    """.strip()
                }
                self._send_json(200, {
                    "status": "ILLUSTRATIVE_SPECIFICATION",
                    "executed": False,
                    "note": "Illustrative analytical query specifications for engineering review; not executed against live production database.",
                    "sql_queries": sql_queries
                })
                return

            # Debug Request Log Endpoint (Proof of wiring)
            if path == "/api/v1/debug/request-log":
                with STATE_LOCK:
                    log_copy = list(APP_STATE.get("request_log", []))
                self._send_json(200, {"count": len(log_copy), "log": log_copy})
                return

            # 7. MySQL 10GB Data Lake Status
            if path == "/api/v1/mysql/status":
                self._send_json(200, APP_STATE["mysql_bridge"])
                return

            # 8. B2B2C Win-Win Features
            if path == "/api/v1/b2b2c/features":
                self._send_json(200, {
                    "count": len(APP_STATE["b2b2c_features"]),
                    "features": APP_STATE["b2b2c_features"]
                })
                return

            # 9. CSV Export: /api/v1/export/red-zone.csv (With CSV formula injection sanitization)
            if path == "/api/v1/export/red-zone.csv":
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["UKID", "Enrollment_No", "Name", "Department", "Semester", "Risk_Score", "Risk_Tier", "Attendance_Pct", "Overdue_Fee_INR", "Curfew_Breaches", "Recommended_Action"])
                
                with STATE_LOCK:
                    students_snapshot = list(APP_STATE["students"])

                for s in students_snapshot:
                    if s["risk_profile"]["tier"] == "HIGH":
                        writer.writerow([
                            sanitize_csv_cell(s["ukid"]),
                            sanitize_csv_cell(s["enrollment_no"]),
                            sanitize_csv_cell(f"{s['first_name']} {s['last_name']}"),
                            sanitize_csv_cell(s["department"]),
                            sanitize_csv_cell(s.get("current_semester", s.get("semester", 5))),
                            sanitize_csv_cell(s["risk_profile"]["score"]),
                            sanitize_csv_cell(s["risk_profile"]["tier"]),
                            sanitize_csv_cell(s["academics"]["overall_attendance_pct"]),
                            sanitize_csv_cell(s["finance"]["amount_overdue"]),
                            sanitize_csv_cell(s["access_gate_telemetry"]["curfew_breaches_30d"]),
                            sanitize_csv_cell(s["risk_profile"].get("recommended_action", "Academic Counseling"))
                        ])
                csv_data = output.getvalue()
                payload = csv_data.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="Digii_Campus_Red_Zone_Cohort.csv"')
                self.send_header("Content-Length", str(len(payload)))
                self.send_header("Connection", "close")
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(payload)
                return

            # 7. Model Validation & Statistical Analytics Endpoint
            if path == "/api/v1/analytics/model-validation":
                with STATE_LOCK:
                    students = list(APP_STATE["students"])
                report = analytics_engine.generate_model_validation_report(students)
                self._send_json(200, report)
                return

            # 8. Transport Routes Query
            if path == "/api/v1/transport/routes":
                routes = database.get_connection().execute("SELECT * FROM transport_routes;").fetchall()
                self._send_json(200, {"count": len(routes), "routes": [dict(r) for r in routes]})
                return

            # 9. Venue Bookings Query
            if path == "/api/v1/venue/bookings":
                venues = database.get_connection().execute("SELECT * FROM venue_bookings;").fetchall()
                self._send_json(200, {"count": len(venues), "venues": [dict(v) for v in venues]})
                return

            # 10. Admissions Matrix Query
            if path == "/api/v1/admissions/matrix":
                matrix = database.get_connection().execute("SELECT * FROM admissions_matrix;").fetchall()
                self._send_json(200, {"count": len(matrix), "matrix": [dict(m) for m in matrix]})
                return

            # Fallback 404 for unknown /api/...
            self._send_json(404, {"error": f"API endpoint not found: {path}"})
            return

        # -------------------------------------------------------------
        # Static UI Serving (Allowlisted Public Directory & Same-Origin)
        # -------------------------------------------------------------
        # Map root / to index.html
        req_rel = path.lstrip("/")
        if req_rel == "" or req_rel == "index.html":
            file_path = INDEX_FILE
            is_initial_page = True
        else:
            file_path = os.path.abspath(os.path.join(PARENT_DIR, unquote(req_rel)))
            is_initial_page = False

        # Enforce canonical path containment within PARENT_DIR
        try:
            common = os.path.commonpath([file_path, PARENT_DIR])
            if common != PARENT_DIR:
                self._send_json(403, {"error": "Forbidden: Path traversal outside root"})
                return
        except ValueError:
            self._send_json(403, {"error": "Forbidden: Path traversal drive mismatch"})
            return

        # Check extension allowlist
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext not in ALLOWED_STATIC_EXTENSIONS:
            self._send_json(403, {"error": f"Forbidden: File type '{ext}' is not publicly accessible"})
            return

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            self._send_json(404, {"error": "File not found"})
            return

        # Read and serve the allowlisted static file
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", ALLOWED_STATIC_EXTENSIONS[ext])
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Connection", "close")
            self._set_cors_headers()

            # If serving the initial HTML page, set HttpOnly SameSite=Strict cookie
            if is_initial_page:
                cookie_str = f"session_token={SESSION_TOKEN}; Path=/; HttpOnly; SameSite=Strict"
                self.send_header("Set-Cookie", cookie_str)

            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self._send_json(500, {"error": "Internal server error"})

    def do_POST(self):
        global AUDIT_COUNTER
        raw_path = self.path
        parsed = urlparse(raw_path)
        path = parsed.path

        with STATE_LOCK:
            APP_STATE.setdefault("request_log", []).append({
                "method": "POST",
                "path": path,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        # Path traversal check on POST
        if "%2e" in raw_path.lower() or ".." in path or "\0" in raw_path:
            self._send_json(403, {"error": "Forbidden: Path traversal detected"})
            return

        # All POST routes require authentication
        if not self._is_authenticated():
            self._send_json(401, {"error": "Unauthorized: Missing or invalid session token cookie"})
            return

        # Safely validate Content-Length header
        cl_raw = self.headers.get("Content-Length")
        if cl_raw is None:
            self._send_json(400, {"error": "Missing Content-Length header"})
            return

        try:
            content_length = int(cl_raw)
        except (ValueError, TypeError):
            self._send_json(400, {"error": "Invalid Content-Length header"})
            return

        if content_length < 0:
            self._send_json(400, {"error": "Negative Content-Length header"})
            return

        # Enforce maximum body size (64 KB)
        if content_length > 65536:
            self._send_json(413, {"error": "Payload too large: Max body size is 64KB"})
            return

        body_data = {}
        if content_length > 0:
            try:
                body_bytes = self.rfile.read(content_length)
                body_data = json.loads(body_bytes.decode("utf-8"))
            except Exception as e:
                self._send_json(400, {"error": f"Invalid JSON payload: {e}"})
                return

        # 1. Action Dispatch Endpoint: /api/v1/students/{ukid}/intervene
        if path.startswith("/api/v1/students/") and path.endswith("/intervene"):
            parts = path.strip("/").split("/")
            if len(parts) == 5 and parts[3].isdigit():
                ukid = int(parts[3])
                with STATE_LOCK:
                    student = next((s for s in APP_STATE["students"] if s["ukid"] == ukid), None)
                    if not student:
                        self._send_json(404, {"error": f"Student UKID {ukid} not found"})
                        return

                    # XSS Sanitization on free text input
                    raw_action = str(body_data.get("action_type", "EMAIL_NUDGE"))
                    raw_notes = str(body_data.get("notes", ""))
                    raw_operator = str(body_data.get("dispatched_by", "Dhruv Jain (Product & Data Architecture Intern)"))

                    action_type = html.escape(raw_action)
                    custom_notes = html.escape(raw_notes)
                    operator = html.escape(raw_operator)

                    # Create Audit Entry with Monotonic ID & DPDP Consent Gating
                    AUDIT_COUNTER += 1
                    audit_id = f"AUD-{AUDIT_COUNTER:06d}"
                    is_guardian = (action_type == "GUARDIAN" or "GUARDIAN" in action_type)
                    consent_certified = bool(body_data.get("consent_certified", not is_guardian))
                    legal_review = is_guardian or bool(body_data.get("legal_review_flagged", False))

                    delivery_meta = {
                        "channel": "SIMULATED",
                        "status": "QUEUED_SIMULATED",
                        "note": "Simulation only; no external network SMS/email dispatched",
                        "dispatched_by": operator,
                        "dpdp_act_2023_aligned": True,
                        "legal_review_flagged": legal_review,
                        "consent_certified": consent_certified
                    }
                    if is_guardian:
                        delivery_meta["statutory_review"] = "Office of Registrar & Legal Counsel flagged for adult student privacy audit under DPDP Act 2023."

                    # Atomic ACID write to persistent SQLite database
                    try:
                        db_record = database.record_intervention(
                            ukid=ukid,
                            action_type=action_type,
                            notes=custom_notes,
                            dispatched_by=operator,
                            consent_verified=consent_certified
                        )
                        if db_record and "id" in db_record:
                            audit_id = db_record["id"]
                    except Exception as e:
                        print(f"[Backend Warning] SQLite intervention record failed: {e}")

                    audit_entry = {
                        "audit_id": audit_id,
                        "ukid": ukid,
                        "student_name": f"{student['first_name']} {student['last_name']}",
                        "enrollment_no": student["enrollment_no"],
                        "action_type": action_type,
                        "dispatched_by": operator,
                        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                        "status": "QUEUED_SIMULATED",
                        "notes": custom_notes,
                        "legal_review_flagged": legal_review,
                        "consent_certified": consent_certified,
                        "delivery_metadata": delivery_meta
                    }
                    APP_STATE["audit_trail"].insert(0, audit_entry)

                    # Append to student's live timeline in memory
                    new_event = {
                        "id": audit_id,
                        "module": "ADMINISTRATIVE_ACTION",
                        "badge": "Action Queued (Simulated)",
                        "title": f"Intervention: {action_type.replace('_', ' ').title()}",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "actor": operator,
                        "description": custom_notes or f"Official proactive retention action ({action_type}) queued for simulated dispatch.",
                        "severity": "SUCCESS"
                    }
                    student.setdefault("timeline_events", []).insert(0, new_event)

                self._send_json(201, {
                    "status": "SUCCESS",
                    "message": f"Action {action_type} successfully logged to simulated audit trail (no external network messages dispatched).",
                    "audit_record": audit_entry
                })
                return

        # 2. Simulate Algorithm Weights: /api/v1/retention/simulate-weights
        if path == "/api/v1/retention/simulate-weights":
            with STATE_LOCK:
                curr_weights = dict(APP_STATE["heuristic_weights"])
                curr_thresh = dict(APP_STATE["risk_thresholds"])
                students_snapshot = list(APP_STATE["students"])

            raw_weights = body_data.get("weights", curr_weights)
            raw_thresholds = body_data.get("thresholds", curr_thresh)

            # Validate weights strictly
            is_valid_w, validated_w, err_w = validate_weights(raw_weights)
            if not is_valid_w:
                self._send_json(400, {"error": f"Invalid weights: {err_w}"})
                return

            # Validate thresholds strictly
            is_valid_th, validated_th, err_th = validate_thresholds(raw_thresholds)
            if not is_valid_th:
                self._send_json(400, {"error": f"Invalid thresholds: {err_th}"})
                return

            # Recalculate for all students in-memory
            recalculated = []
            for s in students_snapshot:
                risk = calculate_student_risk(s, validated_w, validated_th)
                s_copy = dict(s)
                s_copy["risk_profile"] = {
                    **s.get("risk_profile", {}),
                    "score": risk["score"],
                    "tier": risk["tier"],
                    "sub_scores": risk["sub_scores"],
                    "heuristic_risk_index": risk["score"]
                }
                recalculated.append(s_copy)

            red_count = sum(1 for s in recalculated if s["risk_profile"]["tier"] == "HIGH")
            amber_count = sum(1 for s in recalculated if s["risk_profile"]["tier"] == "MEDIUM")
            healthy_count = sum(1 for s in recalculated if s["risk_profile"]["tier"] == "HEALTHY")

            self._send_json(200, {
                "status": "RECALCULATED",
                "weights_used": validated_w,
                "thresholds_used": validated_th,
                "summary": {
                    "red_zone_count": red_count,
                    "amber_zone_count": amber_count,
                    "healthy_count": healthy_count
                },
                "students": recalculated
            })
            return

        # 3. B2B2C Feature Action: /api/v1/b2b2c/action
        if path == "/api/v1/b2b2c/action":
            action_type = body_data.get("action", "UNKNOWN")
            ukid = body_data.get("ukid", 10842)

            # Whitelist validation
            if action_type not in VALID_B2B2C_ACTIONS:
                self._send_json(400, {
                    "error": f"Invalid action '{action_type}'. Valid actions are: {sorted(list(VALID_B2B2C_ACTIONS))}"
                })
                return

            with STATE_LOCK:
                student = next((s for s in APP_STATE["students"] if s["ukid"] == ukid), None)
            if not student:
                self._send_json(404, {"error": f"Student UKID {ukid} not found"})
                return

            result = {
                "status": "SUCCESS",
                "action": action_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "ukid": ukid,
                "student_name": f"{student['first_name']} {student['last_name']}",
                "message": f"Successfully executed concept simulation for: {action_type}"
            }
            self._send_json(200, result)
            return

        # 4. Transport Route Consolidation Endpoint: /api/v1/transport/consolidate
        if path == "/api/v1/transport/consolidate":
            routes = database.consolidate_fleet_routes()
            audit_entry = database.record_intervention(
                ukid=10842,
                action_type="FLEET_ROUTE_CONSOLIDATE",
                dispatched_by="Fleet Operations Manager",
                notes="Route 04 & 09 consolidated into Route 01/07 feeder. Projected diesel savings: ₹2,80,000/mo.",
                consent_verified=True
            )
            with STATE_LOCK:
                APP_STATE["audit_trail"] = database.get_audit_trail()
            self._send_json(200, {
                "status": "CONSOLIDATED",
                "message": "Routes consolidated in persistent transport registry.",
                "routes": routes,
                "audit_record": audit_entry
            })
            return

        # 5. Venue Acoustic Conflict Resolution: /api/v1/venue/resolve-conflict
        if path == "/api/v1/venue/resolve-conflict":
            venues = database.resolve_venue_conflict()
            audit_entry = database.record_intervention(
                ukid=10842,
                action_type="VENUE_ACOUSTIC_RESOLVE",
                dispatched_by="Registrar Infrastructure Office",
                notes="Acoustic sound-bleed resolved by re-allotting band rehearsal to Open Air Amphitheatre.",
                consent_verified=True
            )
            with STATE_LOCK:
                APP_STATE["audit_trail"] = database.get_audit_trail()
            self._send_json(200, {
                "status": "RESOLVED",
                "message": "Auditorium acoustic collision resolved in persistent registry.",
                "venues": venues,
                "audit_record": audit_entry
            })
            return

        # 6. Venue HVAC Pre-Cooling Trigger: /api/v1/venue/hvac-precool
        if path == "/api/v1/venue/hvac-precool":
            venues = database.trigger_hvac_precool()
            audit_entry = database.record_intervention(
                ukid=10842,
                action_type="HVAC_PRECOOL_TRIGGER",
                dispatched_by="Campus Facilities IoT Controller",
                notes="IoT pre-cooling cycle triggered for scheduled auditoriums.",
                consent_verified=True
            )
            with STATE_LOCK:
                APP_STATE["audit_trail"] = database.get_audit_trail()
            self._send_json(200, {
                "status": "PRECOOLED",
                "message": "IoT HVAC pre-cooling cycles triggered.",
                "venues": venues,
                "audit_record": audit_entry
            })
            return

        # 7. Admissions Quota Allotment: /api/v1/admissions/allotment-round
        if path == "/api/v1/admissions/allotment-round":
            matrix = database.run_admissions_allotment()
            audit_entry = database.record_intervention(
                ukid=10842,
                action_type="ADMISSIONS_ROUND_ALLOT",
                dispatched_by="Central Admissions Dean",
                notes="Automated Round 1 seat shifting executed. All vacant quota seats reallocated.",
                consent_verified=True
            )
            with STATE_LOCK:
                APP_STATE["audit_trail"] = database.get_audit_trail()
            self._send_json(200, {
                "status": "ALLOTTED",
                "message": "Admissions quota seats shifted and finalized in database.",
                "matrix": matrix,
                "audit_record": audit_entry
            })
            return

        # 8. Demo State Reset Endpoint: /api/v1/demo/reset
        if path == "/api/v1/demo/reset":
            database.init_database(force_reseed=True)
            load_initial_data()
            with STATE_LOCK:
                total_s = len(APP_STATE["students"])
                audit_c = len(APP_STATE["audit_trail"])
            self._send_json(200, {
                "status": "RESET",
                "message": "Demo state reset successfully: initial student profiles restored, audit counter reset.",
                "total_students": total_s,
                "audit_entries": audit_c
            })
            return

        self._send_json(404, {"error": f"POST endpoint not found: {path}"})

class DigiiCampusServer(ThreadingHTTPServer):
    request_queue_size = 128
    daemon_threads = True

def run_server(port=8000):
    load_initial_data()
    server_address = ("127.0.0.1", port)
    httpd = DigiiCampusServer(server_address, DigiiCampusUnifiedHandler)
    print(f"\n=======================================================")
    print(f"[SERVER] Digii Campus Proactive Retention Unified Server (v2.0)")
    print(f"[STATUS] Serving on http://127.0.0.1:{port}/")
    print(f"[AUTH] Session Token: {SESSION_TOKEN[:8]}... (HttpOnly Cookie Auth)")
    print(f"[STATIC] Allowlisted Static: index.html, data/, assets")
    print(f"[ROUTES] Endpoints:")
    print(f"   - GET  / (Loads index.html with Session Cookie)")
    print(f"   - GET  /api/v1/health")
    print(f"   - GET  /api/v1/students")
    print(f"   - GET  /api/v1/analytics/cohort-summary")
    print(f"   - GET  /api/v1/sql/lineage")
    print(f"   - GET  /api/v1/export/red-zone.csv")
    print(f"   - POST /api/v1/students/<ukid>/intervene")
    print(f"   - POST /api/v1/retention/simulate-weights")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server cleanly...")
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
