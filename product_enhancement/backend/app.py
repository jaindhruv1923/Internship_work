#!/usr/bin/env python3
"""
Digii Campus (CollPoll) — Proactive Retention & Intelligence System API
Phase 4 Backend Service & Algorithmic Heuristic Engine

Author: Dhruv Jain (Product & Data Architecture Intern)
Reporting to: Mr. Suraj Bhatt (Engineering & BI Manager) & Saksham Gupta (Principal Engineer)
Architecture: Zero-Dependency Python 3 RESTful Microservice with in-memory relational state & audit trail
"""

import sys
import os
import json
import csv
import io
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone

# Resolve workspace root and mock data path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PARENT_DIR, "data", "students_mock.json")
SCHEMA_FILE = os.path.join(PARENT_DIR, "data", "schema_definition.json")

# In-Memory State & Audit Log
APP_STATE = {
    "students": [],
    "system_metadata": {},
    "audit_trail": [],
    "heuristic_weights": {
        "academics": 0.35,
        "fees": 0.25,
        "gates": 0.15,
        "hostel": 0.15,
        "chc": 0.10
    },
    "risk_thresholds": {
        "red_zone": 75.0,
        "amber_zone": 50.0
    },
    "mysql_bridge": {
        "service": "MySQL80",
        "port": 3306,
        "host": "localhost",
        "database": "collpoll",
        "status": "ONLINE",
        "table_count": 1647,
        "dump_size_gb": 10.08,
        "latency_ms": 14
    },
    "b2b2c_features": [
        {"id": 1, "title": "Zero-Friction Digital No-Dues", "status": "ACTIVE", "student_win": "Zero waiting outside 10 offices", "university_win": "100% fee clearance before degrees"},
        {"id": 2, "title": "Smart Assignment Deadline Balancer", "status": "ACTIVE", "student_win": "Prevents burnout on Friday overlaps", "university_win": "Higher quality project submissions"},
        {"id": 3, "title": "Verified Digital Auto-Resume Generator", "status": "ACTIVE", "student_win": "Instant verified web portfolio", "university_win": "Placement cell eliminates fake CGPAs"},
        {"id": 4, "title": "Unified Geo-Tagged Maintenance Ticketing", "status": "ACTIVE", "student_win": "Photo room tickets without paper registers", "university_win": "Single-trip repair cluster dispatch"},
        {"id": 5, "title": "Seamless Office Hours Booking System", "status": "ACTIVE", "student_win": "Guaranteed 15-min faculty consultation", "university_win": "Protects professor deep-work hours"},
        {"id": 6, "title": "Automated Medical Leave & CHC Sync", "status": "ACTIVE", "student_win": "No carrying paper slips to 6 professors", "university_win": "Zero fake medical attendance claims"},
        {"id": 7, "title": "AI-Powered Elective & Major Matchmaker", "status": "ACTIVE", "student_win": "Electives matched to past grade strengths", "university_win": "Early predictive classroom capacity sizing"},
        {"id": 8, "title": "Dynamic Campus Marketplace & Lost-and-Found", "status": "ACTIVE", "student_win": "Peer textbook & lab coat savings", "university_win": "Security freed from managing lost items"},
        {"id": 9, "title": "Universal NFC/QR Campus Wallet", "status": "ACTIVE", "student_win": "Phone-only campus survival", "university_win": "Proxy-proof gate & mess consumption data"},
        {"id": 10, "title": "Peer-to-Peer Micro-Tutoring Network", "status": "ACTIVE", "student_win": "Remedial help from peers; credits earned", "university_win": "Higher pass rates without remedial faculty load"}
    ]
}

def load_initial_data():
    """Loads student relational mock dataset and initializes state."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            APP_STATE["students"] = data.get("students", [])
            APP_STATE["system_metadata"] = data.get("system_metadata", {})
            print(f"[Backend] Successfully loaded {len(APP_STATE['students'])} student records from {DATA_FILE}")
    except Exception as e:
        print(f"[Backend Error] Failed loading {DATA_FILE}: {e}")
        APP_STATE["students"] = []

def calculate_student_risk(student, weights=None, thresholds=None):
    """
    Computes normalized Composite Risk Score (CRS) between 0 and 100 based on
    cross-module decay heuristic matching schema from students_mock.json.
    """
    w = weights or APP_STATE["heuristic_weights"]
    th = thresholds or APP_STATE["risk_thresholds"]

    # 1. Academic sub-score (0-100)
    att = student.get("academics", {}).get("overall_attendance_pct", 85.0)
    acad_score = max(0.0, min(100.0, (75.0 - att) * 4.0)) if att < 75.0 else 5.0
    if len(student.get("academics", {}).get("missed_assessments", [])) > 0:
        acad_score = min(100.0, acad_score + 25.0)

    # 2. Finance sub-score (0-100)
    dpd = student.get("finance", {}).get("overdue_days", 0)
    dues = student.get("finance", {}).get("amount_overdue", 0)
    fin_score = 0.0
    if dues > 0:
        fin_score = min(100.0, (dpd / 45.0) * 75.0 + (min(dues, 150000) / 150000.0) * 25.0)

    # 3. Gate telemetry sub-score (0-100)
    gate = student.get("access_gate_telemetry", {})
    curfews = gate.get("curfew_breaches_30d", 0)
    missing_exits = gate.get("missing_exit_logs", 0)
    gate_score = min(100.0, curfews * 20.0 + missing_exits * 15.0)

    # 4. Timeline Event Disciplinary / CHC weight (0-100)
    events = student.get("timeline_events", [])
    critical_events = sum(1 for e in events if e.get("severity") == "CRITICAL")
    warning_events = sum(1 for e in events if e.get("severity") == "WARNING")
    event_score = min(100.0, critical_events * 25.0 + warning_events * 10.0)

    # Weighted Sum
    total_score = (
        w["academics"] * acad_score +
        w["fees"] * fin_score +
        w["gates"] * gate_score +
        (w["hostel"] + w["chc"]) * event_score
    )
    score_int = int(round(total_score))

    # Tier Allocation
    if score_int >= th["red_zone"]:
        tier = "HIGH"
    elif score_int >= th["amber_zone"]:
        tier = "MEDIUM"
    else:
        tier = "HEALTHY"

    return {
        "score": score_int,
        "tier": tier,
        "sub_scores": {
            "academics": round(acad_score, 1),
            "fees": round(fin_score, 1),
            "gates": round(gate_score, 1),
            "events": round(event_score, 1)
        }
    }

class DigiiCampusApiHandler(BaseHTTPRequestHandler):
    """Zero-dependency HTTP Request Handler implementing RESTful JSON APIs."""

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # 1. Healthcheck Endpoint
        if path == "/api/v1/health":
            resp = {
                "status": "UP",
                "service": "Digii Campus Proactive Retention API (BI Portal 2.0)",
                "version": "2.0.0-phase4",
                "active_students": len(APP_STATE["students"]),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 2. Cohort Summary / KPIs
        if path == "/api/v1/analytics/cohort-summary":
            students = APP_STATE["students"]
            red_count = sum(1 for s in students if s["risk_profile"]["tier"] == "HIGH")
            amber_count = sum(1 for s in students if s["risk_profile"]["tier"] == "MEDIUM")
            healthy_count = sum(1 for s in students if s["risk_profile"]["tier"] == "HEALTHY")
            revenue_risk = sum(s["finance"].get("amount_overdue", 0) for s in students if s["risk_profile"]["tier"] == "HIGH")

            resp = {
                "total_active_students": 4850,
                "red_zone_count": red_count,
                "amber_zone_count": amber_count,
                "healthy_count": healthy_count,
                "revenue_at_risk_inr": revenue_risk,
                "revenue_at_risk_formatted": f"₹{revenue_risk/100000:.2f} Lakhs" if revenue_risk < 10000000 else f"₹{revenue_risk/10000000:.2f} Cr",
                "weights_active": APP_STATE["heuristic_weights"],
                "thresholds_active": APP_STATE["risk_thresholds"]
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 3. Students List (with filter support)
        if path == "/api/v1/students":
            tier_filter = query.get("tier", [None])[0]
            dept_filter = query.get("dept", [None])[0]
            search_query = query.get("q", [None])[0]

            filtered = APP_STATE["students"]
            if tier_filter and tier_filter.upper() != "ALL":
                filtered = [s for s in filtered if s["risk_profile"]["tier"] == tier_filter.upper()]
            if dept_filter and dept_filter.upper() != "ALL":
                filtered = [s for s in filtered if s["department"].upper() == dept_filter.upper()]
            if search_query:
                sq = search_query.lower()
                filtered = [s for s in filtered if sq in s["first_name"].lower() or sq in s["last_name"].lower() or sq in s["enrollment_no"].lower()]

            self._set_headers(200)
            self.wfile.write(json.dumps({"count": len(filtered), "students": filtered}).encode("utf-8"))
            return

        # 4. Student Detail by UKID: /api/v1/students/{ukid}
        if path.startswith("/api/v1/students/"):
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[3].isdigit():
                ukid = int(parts[3])
                student = next((s for s in APP_STATE["students"] if s["ukid"] == ukid), None)
                if student:
                    self._set_headers(200)
                    self.wfile.write(json.dumps(student).encode("utf-8"))
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": f"Student UKID {ukid} not found"}).encode("utf-8"))
                return

        # 5. Audit Trail History
        if path == "/api/v1/audit/trail":
            ukid_filter = query.get("ukid", [None])[0]
            logs = APP_STATE["audit_trail"]
            if ukid_filter and ukid_filter.isdigit():
                logs = [l for l in logs if l.get("ukid") == int(ukid_filter)]
            self._set_headers(200)
            self.wfile.write(json.dumps({"count": len(logs), "audit_trail": logs}).encode("utf-8"))
            return

        # 6. SQL Lineage Repository Endpoint (Behind the Data)
        if path == "/api/v1/sql/lineage":
            sql_queries = {
                "kpi_aggregation": """
-- 1. Red Zone Executive Summary Aggregation (CollPoll 270-Table Schema)
SELECT 
    COUNT(DISTINCT u.ukid) AS total_cohort,
    COUNT(DISTINCT CASE WHEN crs.composite_score >= 75 THEN u.ukid END) AS red_zone_count,
    COUNT(DISTINCT CASE WHEN crs.composite_score BETWEEN 50 AND 74 THEN u.ukid END) AS amber_zone_count,
    SUM(CASE WHEN crs.composite_score >= 75 THEN dv.amount_due ELSE 0 END) AS revenue_at_risk_inr
FROM student u
INNER JOIN collpoll_composite_retention_scores crs ON u.ukid = crs.ukid
LEFT JOIN dues_v2 dv ON u.ukid = dv.student_ukid AND dv.status = 'OVERDUE';
                """.strip(),
                "student_360_timeline": """
-- 2. Student 360 Unified Chronological Activity Feed (Grounded in CollPoll Production Tables)
SELECT 'ACADEMIC' AS domain, ca.session_date AS event_time, 'Lecture Absence' AS title, CONCAT('Missed ', c.course_name) AS description
FROM classroom_attendance ca
JOIN course c ON ca.course_id = c.id WHERE ca.student_ukid = :student_ukid AND ca.status = 'ABSENT'
UNION ALL
SELECT 'FINANCE' AS domain, dv.due_date AS event_time, 'Fee Installment Overdue' AS title, CONCAT('Pending: ₹', dv.amount_due) AS description
FROM dues_v2 dv WHERE dv.student_ukid = :student_ukid AND dv.status = 'OVERDUE'
UNION ALL
SELECT 'GATEPASS' AS domain, gpl.in_entry AS event_time, 'Curfew Breach Alert' AS title, CONCAT('Late Gate Entry - Status: ', gps.status_name) AS description
FROM gate_pass_log gpl
JOIN gate_pass_status gps ON gpl.status_id = gps.id WHERE gpl.student_ukid = :student_ukid AND gpl.status_id IN (3, 4)
UNION ALL
SELECT 'CHC' AS domain, cr.created_at AS event_time, 'Service Request Logged' AS title, CONCAT('CHC: ', cs.service_name, ' (Status: ', cr.status, ')') AS description
FROM chc_request cr
JOIN chc_service cs ON cr.service_id = cs.id WHERE cr.requester_ukid = :student_ukid
ORDER BY event_time DESC LIMIT 20;
                """.strip()
            }
            self._set_headers(200)
            self.wfile.write(json.dumps({"sql_queries": sql_queries}).encode("utf-8"))
            return

        # 8. MySQL 10GB Data Lake Status: /api/v1/mysql/status
        if path == "/api/v1/mysql/status":
            self._set_headers(200)
            self.wfile.write(json.dumps(APP_STATE["mysql_bridge"]).encode("utf-8"))
            return

        # 9. B2B2C Win-Win Features: /api/v1/b2b2c/features
        if path == "/api/v1/b2b2c/features":
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "count": len(APP_STATE["b2b2c_features"]),
                "features": APP_STATE["b2b2c_features"]
            }).encode("utf-8"))
            return

        # 7. CSV Export: /api/v1/export/red-zone.csv
        if path == "/api/v1/export/red-zone.csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["UKID", "Enrollment_No", "Name", "Department", "Semester", "Risk_Score", "Risk_Tier", "Attendance_Pct", "Overdue_Fee_INR", "Curfew_Breaches", "Recommended_Action"])
            for s in APP_STATE["students"]:
                if s["risk_profile"]["tier"] == "HIGH":
                    writer.writerow([
                        s["ukid"],
                        s["enrollment_no"],
                        f"{s['first_name']} {s['last_name']}",
                        s["department"],
                        s.get("current_semester", s.get("semester", 5)),
                        s["risk_profile"]["score"],
                        s["risk_profile"]["tier"],
                        s["academics"]["overall_attendance_pct"],
                        s["finance"]["amount_overdue"],
                        s["access_gate_telemetry"]["curfew_breaches_30d"],
                        s["risk_profile"]["recommended_action"]
                    ])
            csv_data = output.getvalue()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header("Content-Disposition", 'attachment; filename="Digii_Campus_Red_Zone_Cohort.csv"')
            self.end_headers()
            self.wfile.write(csv_data.encode("utf-8"))
            return

        # Fallback 404
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": f"API endpoint not found: {path}"}).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Read JSON Body
        content_length = int(self.headers.get("Content-Length", 0))
        body_data = {}
        if content_length > 0:
            try:
                body_bytes = self.rfile.read(content_length)
                body_data = json.loads(body_bytes.decode("utf-8"))
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": f"Invalid JSON payload: {e}"}).encode("utf-8"))
                return

        # 1. Action Dispatch Endpoint: /api/v1/students/{ukid}/intervene
        if path.startswith("/api/v1/students/") and path.endswith("/intervene"):
            parts = path.strip("/").split("/")
            if len(parts) == 5 and parts[3].isdigit():
                ukid = int(parts[3])
                student = next((s for s in APP_STATE["students"] if s["ukid"] == ukid), None)
                if not student:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": f"Student UKID {ukid} not found"}).encode("utf-8"))
                    return

                action_type = body_data.get("action_type", "EMAIL_NUDGE")
                custom_notes = body_data.get("notes", "")
                operator = body_data.get("dispatched_by", "Dhruv Jain (Data & Product Intern)")

                # Create Audit Entry
                audit_entry = {
                    "audit_id": f"AUD-{int(time.time()*1000)}",
                    "ukid": ukid,
                    "student_name": f"{student['first_name']} {student['last_name']}",
                    "enrollment_no": student["enrollment_no"],
                    "action_type": action_type,
                    "dispatched_by": operator,
                    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "status": "DISPATCHED_TO_QUEUE",
                    "notes": custom_notes,
                    "delivery_metadata": {
                        "provider": "Twilio / SendGrid Enterprise Gateway",
                        "response_code": 202,
                        "retries": 0
                    }
                }
                APP_STATE["audit_trail"].insert(0, audit_entry)

                # Append to student's live timeline in memory
                new_event = {
                    "id": audit_entry["audit_id"],
                    "module": "ADMINISTRATIVE_ACTION",
                    "badge": "Action Dispatched",
                    "title": f"Intervention: {action_type.replace('_', ' ').title()}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "actor": operator,
                    "description": custom_notes or f"Official proactive retention action ({action_type}) dispatched.",
                    "severity": "SUCCESS"
                }
                student["timeline_events"].insert(0, new_event)

                self._set_headers(201)
                self.wfile.write(json.dumps({
                    "status": "SUCCESS",
                    "message": f"Action {action_type} successfully dispatched and logged to audit trail.",
                    "audit_record": audit_entry
                }).encode("utf-8"))
                return

        # 2. Simulate Algorithm Weights: /api/v1/retention/simulate-weights
        if path == "/api/v1/retention/simulate-weights":
            new_weights = body_data.get("weights", APP_STATE["heuristic_weights"])
            new_thresholds = body_data.get("thresholds", APP_STATE["risk_thresholds"])

            # Recalculate for all students in-memory
            recalculated = []
            for s in APP_STATE["students"]:
                risk = calculate_student_risk(s, new_weights, new_thresholds)
                s_copy = dict(s)
                s_copy["risk_profile"] = {
                    **s["risk_profile"],
                    "score": risk["score"],
                    "tier": risk["tier"]
                }
                recalculated.append(s_copy)

            red_count = sum(1 for s in recalculated if s["risk_profile"]["tier"] == "HIGH")
            amber_count = sum(1 for s in recalculated if s["risk_profile"]["tier"] == "MEDIUM")
            healthy_count = sum(1 for s in recalculated if s["risk_profile"]["tier"] == "HEALTHY")

            self._set_headers(200)
            self.wfile.write(json.dumps({
                "status": "RECALCULATED",
                "weights_used": new_weights,
                "thresholds_used": new_thresholds,
                "summary": {
                    "red_zone_count": red_count,
                    "amber_zone_count": amber_count,
                    "healthy_count": healthy_count
                },
                "students": recalculated
            }).encode("utf-8"))
            return

        # 3. B2B2C Feature Action: /api/v1/b2b2c/action
        if path == "/api/v1/b2b2c/action":
            action_type = body_data.get("action", "UNKNOWN")
            ukid = body_data.get("ukid", 10842)
            result = {
                "status": "SUCCESS",
                "action": action_type,
                "timestamp": datetime.now().isoformat(),
                "ukid": ukid,
                "message": f"Successfully executed B2B2C innovation action: {action_type}"
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode("utf-8"))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": f"POST endpoint not found: {path}"}).encode("utf-8"))

def run_server(port=8000):
    load_initial_data()
    server_address = ("", port)
    httpd = HTTPServer(server_address, DigiiCampusApiHandler)
    print(f"\n=======================================================")
    print(f"🚀 Digii Campus Proactive Retention API (BI Portal 2.0)")
    print(f"📡 Serving on http://localhost:{port}/")
    print(f"📋 Endpoints:")
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
