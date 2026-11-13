# Digii Campus Proactive Retention System — Phase 4 Backend & API

## Overview
This directory contains the **Phase 4 RESTful microservice and algorithmic simulation backend** for the **Digii Campus (CollPoll) Proactive Retention System (BI Portal 2.0)**.

Designed by **Dhruv Jain** (Product & Data Architecture Intern) to demonstrate prototype backend integration, automated audit trails, and configurable heuristic scoring to **Mr. Suraj Bhatt** (Engineering & BI Manager) and **Saksham Gupta** (Principal Engineer).

---

## Architectural Highlights
- **Zero-Dependency Architecture:** Engineered using the Python 3 standard library (`http.server`, `urllib.parse`, `json`, `csv`, `datetime`, `unittest`). Runs out of the box on developer machines without requiring `pip install`.
- **Dynamic Heuristic Engine:** Recomputes the Composite Risk Score (CRS) across the 8 mock student records in real time based on adjustable domain weights (Academics, Fees, Turnstiles, Hostel, Campus Help Centre), with macro assumptions modeling an enterprise cohort of 4,850 students.
- **In-Memory Audit Trail (Session-Scoped):** Captures every simulated intervention (Email Nudges, HOD Escalations, Counseling Referrals, Guardian Summons) with monotonic audit identifiers (`AUD-XXXXXX`), operator stamps, and simulated delivery metadata.
- **Data Lineage Integration:** Returns illustrative analytical MySQL query specifications grounded in the 10.08 GB database schema documentation.
- **Export Engine:** Streams RFC 4180-compliant CSV datasets of the at-risk Red Zone cohort for the Academic Senate and Registrar.

---

## REST Endpoints Specification

| Method | Endpoint | Description | Payload / Query Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status and active student count | None |
| `GET` | `/api/v1/analytics/cohort-summary` | Executive KPIs, Red/Amber cohort totals, revenue-at-risk | None |
| `GET` | `/api/v1/students` | Full student list with multi-parameter filtering | `?tier=HIGH&dept=CSE&q=aarav` |
| `GET` | `/api/v1/students/{ukid}` | Detailed 360 profile, cross-module status, timeline | None |
| `POST` | `/api/v1/students/{ukid}/intervene` | Queue simulated intervention action & append to audit trail | `{"action_type": "HOD_ESCALATION", "notes": "..."}` |
| `POST` | `/api/v1/retention/simulate-weights` | Recalculate cohort risk scores with custom weights | `{"weights": {"academics": 0.35, ...}}` |
| `GET` | `/api/v1/audit/trail` | Retrieve chronological audit trail records | `?ukid=10842` |
| `GET` | `/api/v1/sql/lineage` | Retrieve illustrative MySQL queries for CTEs and Lineage | None |
| `GET` | `/api/v1/export/red-zone.csv` | Stream real-time CSV file download of Red Zone cohort | None |
| `GET` | `/api/v1/mysql/status` | Simulated MySQL 10.08 GB data lake stand-in status | None |
| `GET` | `/api/v1/b2b2c/features` | Innovation concepts catalog | None |
| `POST` | `/api/v1/b2b2c/action` | Execute innovation concept simulation | `{"action": "SIMULATE_NO_DUES_CLEARANCE", "ukid": 10842}` |

---

## Running the API Server

```powershell
python backend\app.py 8000
```
Server will start and listen on `http://localhost:8000/`.

---

## Running Automated Unit Tests

The backend includes a comprehensive, multi-tiered `unittest` suite validating student dataset integrity, schema cross-module keys, risk flag detection, algorithmic sensitivity, SQLite WAL persistence, and cryptographic security:

```powershell
# 1. API Endpoints & Contract Tests (13 tests)
python backend\test_api.py

# 2. SQLite WAL Persistence Engine (6 tests)
python backend\test_database.py

# 3. Canonical Risk Scoring Engine (7 tests)
python backend\test_analytics.py

# 4. Security & Cryptographic Access Control (12 tests)
python backend\test_security_suite.py

# 5. Core System Integrity Suite (12 tests)
python backend\test_stage1_integrity.py
```
