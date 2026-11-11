# Digii Campus Proactive Retention System — Phase 4 Backend & API

## Overview
This directory contains the **Phase 4 RESTful microservice and algorithmic simulation backend** for the **Digii Campus (CollPoll) Proactive Retention System (BI Portal 2.0)**.

Designed by **Dhruv Jain** (Product & Data Architecture Intern) to demonstrate enterprise backend integration, automated audit trails, and configurable heuristic scoring to **Mr. Suraj Bhatt** (Engineering & BI Manager) and **Saksham Gupta** (Principal Engineer).

---

## Architectural Highlights
- **Zero-Dependency Architecture:** Engineered using the Python 3 standard library (`http.server`, `urllib.parse`, `json`, `csv`, `datetime`, `unittest`). Runs out of the box on any developer machine or production server without requiring `pip install`.
- **Dynamic Heuristic Engine:** Recomputes the Composite Risk Score (CRS) across the 4,850 student cohort in real time based on adjustable domain weights (Academics, Fees, Turnstiles, Curfews, CHC Health).
- **Persistent In-Memory Audit Trail:** Captures every intervention dispatched (Email Nudges, HOD Escalations, Counseling Referrals, Guardian Summons) with ISO 27001-compliant audit identifiers (`AUD-XXXXXX`), operator stamps, and delivery metadata.
- **Data Lineage Integration:** Directly returns the production MySQL queries developed during the 10.08 GB database audit in Week 4.
- **Export Engine:** Streams RFC 4180-compliant CSV datasets of the at-risk Red Zone cohort for the Academic Senate and Registrar.

---

## REST Endpoints Specification

| Method | Endpoint | Description | Payload / Query Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status and active student count | None |
| `GET` | `/api/v1/analytics/cohort-summary` | Executive KPIs, Red/Amber cohort totals, revenue-at-risk | None |
| `GET` | `/api/v1/students` | Full student list with multi-parameter filtering | `?tier=HIGH&dept=CSE&q=aarav` |
| `GET` | `/api/v1/students/{ukid}` | Detailed 360 profile, cross-module status, timeline | None |
| `POST` | `/api/v1/students/{ukid}/intervene` | Dispatch intervention action & append to audit trail | `{"action_type": "HOD_ESCALATION", "notes": "..."}` |
| `POST` | `/api/v1/retention/simulate-weights` | Recalculate cohort risk scores with custom weights | `{"weights": {"academics": 0.40, ...}}` |
| `GET` | `/api/v1/audit/trail` | Retrieve chronological audit trail records | `?ukid=10842` |
| `GET` | `/api/v1/sql/lineage` | Retrieve production MySQL queries for CTEs and Lineage | None |
| `GET` | `/api/v1/export/red-zone.csv` | Stream real-time CSV file download of Red Zone cohort | None |

---

## Running the API Server

```powershell
python backend\app.py 8000
```
Server will start and listen on `http://localhost:8000/`.

---

## Running Automated Unit Tests

The backend includes a comprehensive `unittest` suite validating student dataset integrity, schema cross-module keys, high-risk flag detection, and algorithmic sensitivity:

```powershell
python backend\test_api.py
```
Output:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK
```
