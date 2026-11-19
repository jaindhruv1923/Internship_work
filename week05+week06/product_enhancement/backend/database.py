#!/usr/bin/env python3
"""
Digii Campus (CollPoll) — Persistent Database Layer
Grounded in CollPoll MySQL Schema Definition (schema_definition.json)
ACID-Compliant SQLite3 with Write-Ahead Logging (WAL) Mode
Zero External Dependencies (Python 3 Standard Library)
"""

import os
import sys
import json
import sqlite3
import threading
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PARENT_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "digii_campus.db")
MOCK_PATH = os.path.join(DATA_DIR, "students_mock.json")

# Thread-local storage for safe SQLite connections across HTTP worker threads
_local = threading.local()

def get_connection():
    """Returns a thread-local SQLite connection with WAL mode enabled."""
    if not hasattr(_local, "conn") or _local.conn is None:
        conn = sqlite3.connect(DB_PATH, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA busy_timeout = 5000;")
        _local.conn = conn
    return _local.conn

def close_connection():
    """Closes thread-local connection if open."""
    if hasattr(_local, "conn") and _local.conn is not None:
        try:
            _local.conn.close()
        except Exception:
            pass
        _local.conn = None

def init_database(force_reseed=False):
    """Initializes tables and seeds initial data from students_mock.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = get_connection()
    with conn:
        # 1. Students Table (CollPoll core tables: student, course, ams_attendance, dues_v2, gate_pass_log, etc.)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            ukid INTEGER PRIMARY KEY,
            enrollment_no TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            gender TEXT,
            program TEXT NOT NULL,
            department TEXT NOT NULL,
            batch TEXT NOT NULL,
            current_year INTEGER,
            current_semester INTEGER,
            section TEXT,
            mentor_faculty TEXT,
            accommodation_type TEXT,
            hostel_block TEXT,
            room_no TEXT,
            avatar_url TEXT,
            risk_score INTEGER NOT NULL,
            risk_tier TEXT NOT NULL,
            raw_data_json TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """)

        # 2. Interventions Table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS interventions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id TEXT UNIQUE NOT NULL,
            ukid INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            dispatched_by TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            guardian_consent_verified INTEGER DEFAULT 0,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (ukid) REFERENCES students(ukid)
        );
        """)

        # 3. Monotonic Audit Trail Table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id TEXT UNIQUE NOT NULL,
            ukid INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            action_type TEXT NOT NULL,
            dispatched_by TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            timestamp TEXT NOT NULL
        );
        """)

        # 4. Configurable Heuristic Weights
        conn.execute("""
        CREATE TABLE IF NOT EXISTS heuristic_weights (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            academics REAL NOT NULL,
            fees REAL NOT NULL,
            gates REAL NOT NULL,
            hostel REAL NOT NULL,
            chc REAL NOT NULL,
            red_threshold REAL NOT NULL,
            amber_threshold REAL NOT NULL,
            updated_at TEXT NOT NULL
        );
        """)

        # 5. Transport Fleet Routes Table (transport_management_v2_route)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS transport_routes (
            id INTEGER PRIMARY KEY,
            route_code TEXT UNIQUE NOT NULL,
            corridor TEXT NOT NULL,
            bus_no TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            allotted INTEGER NOT NULL,
            status TEXT NOT NULL,
            is_waste INTEGER DEFAULT 0
        );
        """)

        # 6. Venue Bookings Table (infra_booking)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS venue_bookings (
            id INTEGER PRIMARY KEY,
            venue_name TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            event_name TEXT NOT NULL,
            sound_db INTEGER NOT NULL,
            hvac_status TEXT NOT NULL,
            conflict_status TEXT NOT NULL
        );
        """)

        # 7. Admissions Quota Matrix Table (admissions_lead & merit_rank_master)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS admissions_matrix (
            id INTEGER PRIMARY KEY,
            program TEXT UNIQUE NOT NULL,
            sanctioned_intake INTEGER NOT NULL,
            general_allotted INTEGER NOT NULL,
            reserved_allotted INTEGER NOT NULL,
            vacant_seats INTEGER NOT NULL,
            cutoff_rank INTEGER NOT NULL
        );
        """)

    # Seed if empty or forced
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students;")
    count = cursor.fetchone()[0]

    if count == 0 or force_reseed:
        seed_data(conn)

def seed_data(conn):
    """Populates database with canonical mock students and module states."""
    with open(MOCK_PATH, "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    now_iso = datetime.now(timezone.utc).isoformat()

    with conn:
        conn.execute("DELETE FROM interventions;")
        conn.execute("DELETE FROM audit_trail;")
        conn.execute("DELETE FROM students;")
        conn.execute("DELETE FROM heuristic_weights;")
        conn.execute("DELETE FROM transport_routes;")
        conn.execute("DELETE FROM venue_bookings;")
        conn.execute("DELETE FROM admissions_matrix;")

        # Insert Students
        for s in mock_data.get("students", []):
            risk = s.get("risk_profile", {})
            conn.execute("""
            INSERT INTO students (
                ukid, enrollment_no, first_name, last_name, email, phone, gender,
                program, department, batch, current_year, current_semester, section,
                mentor_faculty, accommodation_type, hostel_block, room_no, avatar_url,
                risk_score, risk_tier, raw_data_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                s["ukid"],
                s.get("enrollment_no", f"2024CS{s['ukid']}"),
                s.get("first_name", ""),
                s.get("last_name", ""),
                s.get("email", ""),
                s.get("phone", ""),
                s.get("gender", "Unspecified"),
                s.get("program", ""),
                s.get("department", ""),
                s.get("batch", "2024-2028"),
                s.get("current_year", 3),
                s.get("current_semester", 5),
                s.get("section", "A"),
                s.get("mentor_faculty", ""),
                s.get("accommodation_type", "DAY_SCHOLAR"),
                s.get("hostel_block", ""),
                s.get("room_no", ""),
                s.get("avatar_url", ""),
                risk.get("score", 0),
                risk.get("tier", "HEALTHY"),
                json.dumps(s),
                now_iso
            ))

        # Insert Default Weights
        conn.execute("""
        INSERT INTO heuristic_weights (id, academics, fees, gates, hostel, chc, red_threshold, amber_threshold, updated_at)
        VALUES (1, 0.35, 0.25, 0.15, 0.15, 0.10, 75.0, 50.0, ?);
        """, (now_iso,))

        # Initial audit log starts clean (0 records) until interventions occur

        # Seed Transport Routes
        routes = [
            (1, "Route 01: North Corridor", "Rohini -> Pitampura -> Campus", "Bus HR-26-A4910 (42 Seats)", 42, 40, "OPTIMAL (95.2%)", 0),
            (2, "Route 04: West Feeder", "Dwarka Sector 21 -> Janakpuri -> Campus", "Bus HR-26-B1092 (42 Seats)", 42, 16, "LOW LOAD (38.1%)", 1),
            (3, "Route 07: South Express", "Noida Sector 62 -> Mayur Vihar -> Campus", "Bus DL-1V-8942 (52 Seats)", 52, 48, "OPTIMAL (92.3%)", 0),
            (4, "Route 09: Central Shuttle", "Connaught Place -> Dhaula Kuan -> Campus", "Bus HR-26-C8819 (42 Seats)", 42, 14, "LOW LOAD (33.3%)", 1)
        ]
        for r in routes:
            conn.execute("""
            INSERT INTO transport_routes (id, route_code, corridor, bus_no, capacity, allotted, status, is_waste)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, r)

        # Seed Venue Bookings
        venues = [
            (1, "Main University Auditorium (Block A)", 1200, "Annual Cultural Fest Rehearsals", 94, "STANDBY", "ACOUSTIC_COLLISION"),
            (2, "Seminar Hall 1 (Ground Floor, Block A)", 180, "Dean's Research Seminar", 45, "STANDBY", "ACOUSTIC_COLLISION"),
            (3, "Open Air Amphitheatre (North Lawn)", 2500, "Rock Band Soundcheck", 98, "STANDBY", "OPTIMAL"),
            (4, "Tech Innovation Lab (Tech Block)", 120, "Smart India Hackathon Mentoring", 52, "COOLED", "OPTIMAL")
        ]
        for v in venues:
            conn.execute("""
            INSERT INTO venue_bookings (id, venue_name, capacity, event_name, sound_db, hvac_status, conflict_status)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, v)

        # Seed Admissions Matrix
        matrix = [
            (1, "B.Tech Computer Science & Engineering", 360, 240, 110, 10, 16500),
            (2, "B.Tech AI & Data Science", 180, 120, 54, 6, 18200),
            (3, "B.Tech Electronics & Communication", 240, 140, 80, 20, 24500),
            (4, "B.Tech Biotechnology", 120, 70, 35, 15, 31000)
        ]
        for m in matrix:
            conn.execute("""
            INSERT INTO admissions_matrix (id, program, sanctioned_intake, general_allotted, reserved_allotted, vacant_seats, cutoff_rank)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """, m)

    print(f"[Database] SQLite persistence initialized at {DB_PATH} with WAL mode.")

# --- High-Level Query & Mutation APIs ---

def get_students(tier=None, dept=None, query=None):
    """Retrieves students with optional filtering."""
    conn = get_connection()
    sql = "SELECT * FROM students WHERE 1=1"
    params = []

    if tier and tier.upper() != "ALL":
        sql += " AND UPPER(risk_tier) = ?"
        params.append(tier.upper())

    if dept and dept != "ALL":
        sql += " AND department LIKE ?"
        params.append(f"%{dept}%")

    if query:
        sql += " AND (first_name LIKE ? OR last_name LIKE ? OR enrollment_no LIKE ? OR CAST(ukid AS TEXT) LIKE ?)"
        q_wild = f"%{query}%"
        params.extend([q_wild, q_wild, q_wild, q_wild])

    sql += " ORDER BY risk_score DESC;"
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()

    students = []
    for r in rows:
        st = json.loads(r["raw_data_json"])
        st["risk_profile"]["score"] = r["risk_score"]
        st["risk_profile"]["tier"] = r["risk_tier"]
        students.append(st)
    return students

def get_student_by_ukid(ukid):
    """Retrieves single student profile by ukid."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT raw_data_json, risk_score, risk_tier FROM students WHERE ukid = ?;", (ukid,))
    row = cursor.fetchone()
    if not row:
        return None
    st = json.loads(row["raw_data_json"])
    st["risk_profile"]["score"] = row["risk_score"]
    st["risk_profile"]["tier"] = row["risk_tier"]
    return st

def record_intervention(ukid, action_type, dispatched_by, notes, consent_verified=False):
    """Records an intervention and updates audit trail atomically."""
    conn = get_connection()
    now_iso = datetime.now(timezone.utc).isoformat()

    with conn:
        # Determine next monotonic audit ID
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM audit_trail;")
        next_num = 101 + cursor.fetchone()[0]
        audit_id = f"AUD-{next_num:06d}"

        # Get student name
        cursor.execute("SELECT first_name, last_name, raw_data_json FROM students WHERE ukid = ?;", (ukid,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Student UKID {ukid} not found")
        student_name = f"{row['first_name']} {row['last_name']}".strip()

        # Insert Intervention
        conn.execute("""
        INSERT INTO interventions (audit_id, ukid, action_type, dispatched_by, status, notes, guardian_consent_verified, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            audit_id,
            ukid,
            action_type,
            dispatched_by,
            "QUEUED_SIMULATED",
            notes,
            1 if consent_verified else 0,
            now_iso
        ))

        # Insert Audit Record
        conn.execute("""
        INSERT INTO audit_trail (audit_id, ukid, student_name, action_type, dispatched_by, status, notes, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            audit_id,
            ukid,
            student_name,
            action_type,
            dispatched_by,
            "QUEUED_SIMULATED",
            notes,
            now_iso
        ))

        # Append timeline event to raw JSON
        st = json.loads(row["raw_data_json"])
        st.setdefault("timeline_events", []).append({
            "id": f"EVT-{audit_id}",
            "timestamp": now_iso,
            "module": "INTERVENTION_DISPATCH",
            "severity": "CRITICAL" if "GUARDIAN" in action_type or "HOD" in action_type else "WARNING",
            "title": f"Action Executed: {action_type.replace('_', ' ').title()}",
            "description": f"{notes} (Dispatched by {dispatched_by})",
            "badge": "Action Center",
            "icon": "mail_nudge",
            "actor": dispatched_by
        })
        conn.execute("UPDATE students SET raw_data_json = ?, updated_at = ? WHERE ukid = ?;", (json.dumps(st), now_iso, ukid))

    return {
        "audit_id": audit_id,
        "ukid": ukid,
        "action_type": action_type,
        "dispatched_by": dispatched_by,
        "status": "QUEUED_SIMULATED",
        "notes": notes,
        "guardian_consent_verified": consent_verified,
        "timestamp": now_iso
    }

def get_audit_trail(ukid=None):
    """Retrieves chronological audit trail records."""
    conn = get_connection()
    cursor = conn.cursor()
    if ukid:
        cursor.execute("SELECT * FROM audit_trail WHERE ukid = ? ORDER BY id DESC;", (ukid,))
    else:
        cursor.execute("SELECT * FROM audit_trail ORDER BY id DESC;")
    rows = cursor.fetchall()
    return [dict(r) for r in rows]

def get_weights_and_thresholds():
    """Retrieves current heuristic weights and risk thresholds."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM heuristic_weights WHERE id = 1;")
    row = cursor.fetchone()
    if not row:
        return {"academics": 0.35, "fees": 0.25, "gates": 0.15, "hostel": 0.15, "chc": 0.10}, {"red_zone": 75.0, "amber_zone": 50.0}
    weights = {
        "academics": row["academics"],
        "fees": row["fees"],
        "gates": row["gates"],
        "hostel": row["hostel"],
        "chc": row["chc"]
    }
    thresholds = {
        "red_zone": row["red_threshold"],
        "amber_zone": row["amber_threshold"]
    }
    return weights, thresholds

def update_weights(weights, thresholds):
    """Persists updated weights and thresholds."""
    conn = get_connection()
    now_iso = datetime.now(timezone.utc).isoformat()
    with conn:
        conn.execute("""
        UPDATE heuristic_weights SET
            academics = ?, fees = ?, gates = ?, hostel = ?, chc = ?,
            red_threshold = ?, amber_threshold = ?, updated_at = ?
        WHERE id = 1;
        """, (
            weights["academics"], weights["fees"], weights["gates"], weights["hostel"], weights["chc"],
            thresholds["red_zone"], thresholds["amber_zone"], now_iso
        ))

def update_student_scores(scored_students):
    """Updates computed risk scores across students in SQLite."""
    conn = get_connection()
    now_iso = datetime.now(timezone.utc).isoformat()
    with conn:
        for s in scored_students:
            risk = s["risk_profile"]
            conn.execute("""
            UPDATE students SET
                risk_score = ?, risk_tier = ?, raw_data_json = ?, updated_at = ?
            WHERE ukid = ?;
            """, (risk["score"], risk["tier"], json.dumps(s), now_iso, s["ukid"]))

# --- Secondary Modules Database Operations ---

def consolidate_fleet_routes():
    """Consolidates underutilized bus routes (Route 04 & 09) into Route 01/07."""
    conn = get_connection()
    with conn:
        conn.execute("""
        UPDATE transport_routes SET
            corridor = 'Sector 56 -> Cyber City -> Campus (Consolidated Feeder)',
            status = 'CONSOLIDATED (OPTIMAL 88%)',
            allotted = 37,
            is_waste = 0
        WHERE id = 2;
        """)
        conn.execute("""
        UPDATE transport_routes SET
            status = 'VEHICLE IDLE (DIESEL SAVED)',
            allotted = 0,
            is_waste = 0
        WHERE id = 4;
        """)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transport_routes;")
    return [dict(r) for r in cursor.fetchall()]

def resolve_venue_conflict():
    """Resolves auditorium acoustic sound-bleed by re-allotting band rehearsals to Open Air Amphitheatre."""
    conn = get_connection()
    with conn:
        conn.execute("""
        UPDATE venue_bookings SET
            event_name = 'Re-Allotted to Open Air Theatre (OAT North)',
            sound_db = 45,
            conflict_status = 'RESOLVED (ZERO COLLISION)'
        WHERE id = 2;
        """)
        conn.execute("""
        UPDATE venue_bookings SET
            conflict_status = 'OPTIMAL (SOUND CONTAINED)'
        WHERE id = 1;
        """)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM venue_bookings;")
    return [dict(r) for r in cursor.fetchall()]

def trigger_hvac_precool():
    """Triggers IoT pre-cooling cycle for scheduled halls."""
    conn = get_connection()
    with conn:
        conn.execute("""
        UPDATE venue_bookings SET
            hvac_status = 'PRE-COOLED (21 C Target Achieved)'
        WHERE id IN (1, 2, 4);
        """)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM venue_bookings;")
    return [dict(r) for r in cursor.fetchall()]

def run_admissions_allotment():
    """Shifts vacant quota seats into general merit pool."""
    conn = get_connection()
    with conn:
        conn.execute("""
        UPDATE admissions_matrix SET
            general_allotted = general_allotted + vacant_seats,
            vacant_seats = 0;
        """)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admissions_matrix;")
    return [dict(r) for r in cursor.fetchall()]

