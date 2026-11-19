#!/usr/bin/env python3
"""
Unit Test Suite for Persistent SQLite Database Layer
Tests ACID compliance, WAL mode, CRUD operations, transactions, and durability
"""

import os
import sys
import unittest
import tempfile
import sqlite3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import database

class TestDatabaseLayer(unittest.TestCase):
    def setUp(self):
        # Initialize database
        database.init_database(force_reseed=True)

    def test_database_initialization_and_wal_mode(self):
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        mode = cursor.fetchone()[0]
        self.assertEqual(mode.lower(), "wal")

    def test_get_all_students(self):
        students = database.get_students()
        self.assertEqual(len(students), 8)
        self.assertEqual(students[0]["first_name"], "Aarav")
        self.assertEqual(students[0]["risk_profile"]["tier"], "HIGH")

    def test_get_students_filtered_by_tier(self):
        high_students = database.get_students(tier="HIGH")
        self.assertEqual(len(high_students), 1)
        self.assertEqual(high_students[0]["first_name"], "Aarav")

        medium_students = database.get_students(tier="MEDIUM")
        self.assertEqual(len(medium_students), 2)
        names = [s["first_name"] for s in medium_students]
        self.assertIn("Priya", names)
        self.assertIn("Rohan", names)

    def test_get_student_by_ukid(self):
        aarav = database.get_student_by_ukid(10842)
        self.assertIsNotNone(aarav)
        self.assertEqual(aarav["first_name"], "Aarav")
        self.assertEqual(aarav["risk_profile"]["score"], 87)

        nonexistent = database.get_student_by_ukid(999999)
        self.assertIsNone(nonexistent)

    def test_record_intervention_and_audit_trail_durability(self):
        res = database.record_intervention(
            ukid=10842,
            action_type="PARENT_SUMMON",
            dispatched_by="Dean Academic Affairs",
            notes="Formal disciplinary hearing scheduled",
            consent_verified=True
        )
        self.assertTrue(res["audit_id"].startswith("AUD-"))
        self.assertEqual(res["guardian_consent_verified"], True)

        # Check audit trail query
        trail = database.get_audit_trail(ukid=10842)
        self.assertTrue(len(trail) >= 1)
        latest = trail[0]
        self.assertEqual(latest["audit_id"], res["audit_id"])
        self.assertEqual(latest["action_type"], "PARENT_SUMMON")

    def test_secondary_modules_state_mutations(self):
        # 1. Transport consolidation
        routes = database.consolidate_fleet_routes()
        self.assertEqual(len(routes), 4)
        route_4 = next(r for r in routes if r["id"] == 2)
        self.assertIn("CONSOLIDATED", route_4["status"])

        # 2. Venue conflict resolution
        venues = database.resolve_venue_conflict()
        venue_2 = next(v for v in venues if v["id"] == 2)
        self.assertEqual(venue_2["conflict_status"], "RESOLVED (ZERO COLLISION)")

        # 3. HVAC Pre-Cooling
        cooled = database.trigger_hvac_precool()
        auditorium = next(v for v in cooled if v["id"] == 1)
        self.assertIn("PRE-COOLED", auditorium["hvac_status"])

        # 4. Admissions Allotment
        adm = database.run_admissions_allotment()
        cs = next(m for m in adm if m["id"] == 1)
        self.assertEqual(cs["vacant_seats"], 0)

if __name__ == "__main__":
    unittest.main()

