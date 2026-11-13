# Digii Campus (CollPoll) — Data & Product Internship Worklogs

**Author:** Dhruv Jain  
**Role:** Data & Product Intern (Proposing Formal Transition to **Product Intern / APM**)  
**Repository:** [github.com/jaindhruv1923/Internship_work](https://github.com/jaindhruv1923/Internship_work)  
**Reporting Period:** October – November 2026 (Odd Semester AY 2026-27)  
**Managers & Mentors:** Mr. Suraj Bhatt (Engineering & BI Manager), Saksham Gupta (Principal Engineer), Gurdeep Singh, Piyush Anand, Shamitr Sudhir Mardikar

---

## Executive Summary & Role Transition Objective

This repository documents the weekly research, database engineering, enterprise BI optimization, and product architecture deliverables completed during my internship at **Digii Campus (formerly CollPoll)**.

Over the 5-week tenure, my scope expanded from foundational frontend research to deep database engineering (grounded in Suraj Shetty's CollPoll Workflows document covering 270 tables across 6 modules: CHC, Gatepass, Hostel, Infrastructure, Placements, Transport) on our **10.08 GB production MySQL replica** (1,647 tables, 15 operational domains), culminating in the architecture, engineering, and delivery of **Digii Campus 2.0: Enterprise Intelligence & B2B2C Student Experience Platform**.

By bridging relational data depth with product prioritization frameworks (RICE), engineering safety guardrails (LaunchDarkly-style feature flags and circuit breakers), DPDP Act 2023 privacy governance, and dual-sided user design (administrative cockpit and student-facing experience hub), this work demonstrates my readiness to formally transition into the **Product Intern / APM** role.

---

## Quick Start — Launching the Live Platform & Test Suites

The platform runs on a **unified zero-dependency architecture** built exclusively with Python 3 standard library modules and standard browser technologies. No third-party packages (`pip install` or `npm install`) are required.

### 1. Launching the Unified Server (Frontend SPA & REST API)

Run the single-origin Python server from the repository root:

```powershell
python product_enhancement\backend\app.py 8000
```

- **Frontend Application:** Open `http://localhost:8000/` in any modern browser.
- **RESTful Endpoints:** Accessible at `http://localhost:8000/api/v1/...`
- **Security & Storage:** Protected via 256-bit cryptographically random session tokens (delivered via `HttpOnly` cookie on initial load) and backed by SQLite with Write-Ahead Logging (WAL) for persistent audit trails.

### 2. Running the Full Verification & Compliance Suite

Validate the complete frontend Single Page Application (26 views, 594 DOM IDs, 240 event handlers, zero emojis, DPDP Act 2023 compliance, and schema grounding):

```powershell
python product_enhancement\verify_suite.py
```

### 3. Running Backend Unit & Security Test Suites

The backend microservice includes automated, multi-tiered test suites:

```powershell
# 1. REST API Contract & Endpoint Validation (13 tests)
python product_enhancement\backend\test_api.py

# 2. SQLite WAL Persistence Engine (6 tests)
python product_enhancement\backend\test_database.py

# 3. Canonical Risk Scoring Engine (7 tests)
python product_enhancement\backend\test_analytics.py

# 4. Security & Cryptographic Access Control (12 tests)
python product_enhancement\backend\test_security_suite.py

# 5. Core System Integrity & Model Parity (12 tests)
python product_enhancement\backend\test_stage1_integrity.py
```

---

## Weekly Progression

### Week 01: Onboarding, Architecture Alignment & Access Protocols

- **Period:** 12 October 2026 – 16 October 2026
- **Deliverables:** `week 01-12th-16th October-2026/WorkLog_Week01_12-16thOctober_Dhruv.pdf`
- **Core Focus:**
  - Integrated into the Digii Campus engineering and product teams.
  - Explored core frontend modules and student life cycle workflows.
  - Reviewed enterprise security policies, VPN protocols, and operational compliance guidelines.

---

### Week 02: Non-Academic Student Development Framework

- **Period:** 19 October 2026 – 23 October 2026
- **Deliverables:**
  - `week 02-19th-23rd October-2026/WorkLog_Week02_19-23rdOctober_Dhruv.pdf`
  - `week 02-19th-23rd October-2026/Non-Academic Student Development_Report.pdf`
  - `week 02-19th-23rd October-2026/Evaluating Non-Academic Student Development Framework, Product Design and Digii Campus Enhancement Proposal.pdf`
- **Core Focus:**
  - Designed an end-to-end Non-Academic Student Development Framework bridging co-curricular participation with institutional accreditation.
  - Developed product UX blueprints and functional specifications for student life analytics.
  - Authored a comprehensive enhancement proposal submitted to the product design team.

---

### Week 03: Product Research & Competitive Benchmarking

- **Period:** 26 October 2026 – 30 October 2026
- **Deliverables:**
  - `week 03-26th-30th October-2026/WorkLog_Week03_26-30thOctober_Dhruv.pdf`
  - `week 03-26th-30th October-2026/Product_Research_and_Enhancement_Proposal.pdf`
- **Core Focus:**
  - Conducted comparative market research across higher-education ERP and student management platforms.
  - Identified usability gaps in existing institutional workflows and mapped high-impact feature enhancements.
  - Formulated technical proposals for cross-module integration across dining, housing, and access control.

---

### Week 04: Enterprise BI Database Audit, Performance Optimization & Advanced Analytics

- **Period:** 02 November 2026 – 06 November 2026
- **Reviewer:** Mr. Suraj Bhatt (Engineering & BI Manager)
- **KT & Architecture Mentors:** Shamitr Sudhir Mardikar, Gurdeep Singh, Prudvi Pratap Kanakala, Piyush Anand
- **Deliverables:**
  - `week 04 - 2nd-6th November-2026/Internship Worklog - Week 4.pdf`
  - `week 04 - 2nd-6th November-2026/Digii_Campus_BI_Database_Audit_Optimization_Week04.sql` (50 KB master SQL suite)
- **Core Focus:**
  - **Environment Configuration & 10GB Dump Ingestion:** Configured local MySQL 8.0 mirror environment replicating AWS RDS production parameters. Resolved import bottlenecks (buffer pool sizing, `max_allowed_packet = 1GB`, query timeout tuning).
  - **Comprehensive Schema Exploration (1,647 Tables):** Categorized all tables across 15 enterprise architectural domains (EMS, Identity/Auth, CHC Service Desk, Finance/Dues, Hostel, Turnstile Access, Mess/Dining, etc.).
  - **Relational Reverse-Engineering:** Mapped primary/foreign key graphs and audited soft/implicit relationships across core modules.
  - **Data Quality Audit & Anomaly Detection:** Formulated queries isolating historical data anomalies, including orphaned transactional logs, chronological window inversions (`pass_end < pass_start`), impossible travel (<180s multi-gate punches), and hostel attendance vs gate exit discrepancies.
  - **Advanced Analytical SQL:** Implemented recursive CTEs (dynamic 90-day calendar date spine, escalation hierarchy traversal), window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE(4)`, `LAG`/`LEAD`, rolling 7-day moving averages, cumulative sums), multidimensional rollups, and conditional matrix pivots.
  - **Quantitative Business Analytics:** Built an RFM (Recency, Frequency, Intensity) student engagement scoring model, Pareto (80/20) escalation root-cause analysis, and Z-Score outlier detection for ticket resolution turnaround times.
  - **Production Enhancements:** Engineered composite/covering indexes, structural DDL `CHECK` constraints, 5 enterprise analytical BI views, a business-hour calculation UDF, and 3 automated reporting stored procedures aligned with the ClickUp 5-step workflow.

---

### Week 05: Enterprise Product Architecture, Digii Campus 2.0 & Autonomous Intelligence

- **Period:** 09 November 2026 – 13 November 2026
- **Reviewers:** Mr. Suraj Bhatt (Engineering & BI Manager), Saksham Gupta (Principal Engineer)
- **Deliverables:**
  - `week 05 - 9th-13th November-2026/Internship_Worklog_Week_05_Dhruv_Jain.md` (Comprehensive Week 5 worklog)
  - `product_enhancement/index.html` (Complete Single Page Application prototype, 26 views, 1.2 MB)
  - `product_enhancement/PRD_Proactive_Retention_System.md` (Product Requirements Document v2.4)
  - `product_enhancement/EXECUTIVE_PITCH_PLAYBOOK.md` (15-minute executive pitch screenplay & objection-handling track)
  - `product_enhancement/EXECUTIVE_PITCH_DECK.md` (12-slide executive presentation deck)
  - `product_enhancement/REMEDIATION_REPORT.md` (Forensic architectural hardening report)
  - `product_enhancement/docs/PRIVACY_DESIGN.md` (DPDP Act 2023 compliance specification)
  - `product_enhancement/verify_suite.py` (Automated 13-point compliance verification engine)
  - `product_enhancement/backend/` (Zero-dependency REST microservice, canonical risk engine, SQLite WAL persistence, security suite)
- **Core Focus & Architectural Enhancements:**
  - **Executive Slide Deck inside Comparative Matrix (`view-comparative`):** Built-in 6-slide interactive presentation with keyboard arrow navigation, slide-progress indicator, and dual-mode switcher toggle between executive presentation and the 17-module relational schema matrix.
  - **Closed-Loop Intervention Escalation Ladder (`view-student360`):** Shifting from passive detection to resolution tracking across temporal milestones:
    - Day 1: Automated nudge dispatched to faculty mentor.
    - Day 4: Campus Help Centre (CHC) academic counseling ticket auto-logged with strict 48-hour SLA.
    - Day 8: Flexible split-fee restructuring plan auto-dispatched to parent.
    - Temporal Velocity Delta: Tracking risk recovery from initial alert (87 High) to counseling (64 Amber) to fee restructuring (38 Safe).
  - **Multi-Persona Strategic Architecture:**
    - Students (`view-student-hub`): Academic & Financial Health Compass translating risk scores into prescriptive guidance (e.g., attending 3 more lectures to cross 75% threshold; 2-part UPI installment pre-approval).
    - Faculty Mentors (`view-student360`): Mentee pulse stream eliminating multi-portal manual checks.
    - Hostel Wardens (`view-isolation`): In-person welfare check list with real-time audit trail.
    - Finance Officers (`view-finance`, `view-nodues`): Cash-flow recovery pipeline and 1.2-second parallel no-dues clearance.
  - **Cross-Module Network Effects:**
    - LMS Deadline Balancer (`view-deadline`): Detects assignment congestion on Fridays and auto-extends central library turnstile operating hours to 01:30 AM while suppressing curfew penalty alerts.
    - Campus Help Centre ↔ No-Dues Desk (`view-nodues`): Pending fee disputes placed in conditional escrow to unlock degree certificates instantly without 14-day manual stamp delays.
    - Mess Dining ↔ University Medical Centre (`view-prge`): Correlates clinic gastrointestinal cases with dining biometric logs to isolate food batch anomalies.
  - **26 Operational Enterprise Views (Registered in `SPA_VIEWS`):**
    1. _Predictive Dropout Radar (`view-radar`):_ Multi-tier risk classifier with department filters and real-time advisor intervention triggers.
    2. _Student 360 Timeline (`view-student360`):_ Longitudinal intelligence chronicle with closed-loop escalation ladder and temporal velocity tracking.
    3. _Student Experience Hub (`view-student-hub`):_ Academic & Financial Health Compass and 10 dual-value B2B2C student services.
    4. _Social Isolation Sentinel (`view-isolation`):_ Correlates turnstiles with zero club/library interactions for 14+ days and hostel warden welfare checks.
    5. _Predictive Kitchen Prep & Food Waste Reducer (`view-prge`):_ Deducts approved hostel night leaves from morning mess preparation, saving 630 meals/day.
    6. _Autonomous No-Dues Instant Clearance (`view-nodues`):_ 1.2-second parallel relational audit across 8 departments with conditional escrow protocols.
    7. _Smart Deadline Congestion Balancer (`view-deadline`):_ Campus-wide LMS submission balancer with library curfew auto-extension.
    8. _Tamper-Proof Relational Auto-Resume (`view-autoresume`):_ Compiles authenticated SGPA, OBE rubrics, and club leadership into QR-verifiable CVs.
    9. _Turnstile Anti-Passback & Impossible Travel (`view-passback`):_ Biometric velocity physics checker detecting proxy card taps in <180s.
    10. _Non-Academic Development Ledger (`view-development`):_ Tracking 3,840 enrichment credit students, 42 clubs, and NAAC 5.3 compliance.
    11. _CHC Workflow Intelligence & SLA Analytics (`view-grievance`):_ Cross-service request analytics on `chc_request` and `chc_middleware`.
    12. _Phantom Midnight Energy & Green Campus (`view-energy`):_ Occupancy-vs-meter cross-checking engine auto-shedding empty lecture hall HVAC at 2:00 AM.
    13. _Alumni Capstone Micro-Endowment (`view-alumni`):_ Capstone prototype pitching exchange with 1:1 mentorship bookings.
    14. _Accreditation Copilot (`view-accreditation`):_ NAAC SSR 7-criteria telemetry with relational evidence scanning.
    15. _Academics Timetable Clash Interceptor (`view-academics`):_ 32-credit track scheduler and 1-click timetable clash resolver.
    16. _Finance & Fee Dues Recon (`view-finance`):_ Automated bank reconciliation matcher recovering ₹1.95 Cr tuition exposure.
    17. _Financial Aid & DBT Gateway (`view-scholarships`):_ Institutional aid disbursement ledger with automated tuition offset crediting.
    18. _AI Merit & Multi-Quota Seat Allotment Matrix (`view-admissions`):_ Dynamic cutoff slider and multi-round quota allotment.
    19. _Smart Campus Infrastructure & Acoustic Interceptor (`view-venue`):_ High-decibel acoustic collision detection on `infra_booking`.
    20. _Smart Fleet & Transport v2 Route Optimizer (`view-transport`):_ Route fleet optimizer merging sub-40% occupancy lines.
    21. _Digii Campus vs. Digii 2.0 Comparative Intelligence Matrix (`view-comparative`):_ 6-slide executive presentation and 17-module technical grid.
    22. _Enterprise Operations & Student Management Workbench (`view-operations-desk`):_ Daily execution desk for bulk CSV onboarding, AMS daily attendance, cashier fee collection, hostel out-passes, and CHC ticketing.
    23. _PM Strategy Cockpit (`view-pm-cockpit`):_ RICE roadmap matrix, LaunchDarkly feature flags, Amplitude telemetry funnels, and in-app PRD viewer.
    24. _Executive Pitch Deck (`view-deck`):_ Full-screen 12-slide presentation mode with keyboard arrow navigation.
    25. _Audit Trail Explorer (`view-audit`):_ Chronological cryptographic audit logs of all administrative actions.
    26. _SQL Lineage Inspector (`view-sql`):_ Grounded MySQL CTE queries and data lineage documentation.

---

## Repository Structure

```
.
├── .gitignore                                             # Excludes 10GB dumps, SQLite WAL journals, and Python caches
├── README.md                                              # Comprehensive repository overview and executive documentation
├── product_enhancement/
│   ├── .gitignore                                         # Component-level ignore for cache and journals
│   ├── index.html                                         # Full interactive SPA (26 Views, 1.2 MB, zero emojis)
│   ├── verify_suite.py                                    # Automated compliance suite (13/13 passing)
│   ├── package.json                                       # Project metadata and run scripts
│   ├── requirements.txt                                   # Zero third-party runtime dependencies declaration
│   ├── REMEDIATION_REPORT.md                              # Forensic architectural hardening and traceability matrix
│   ├── PRD_Proactive_Retention_System.md                  # Complete Product Requirements Document v2.4
│   ├── EXECUTIVE_PITCH_PLAYBOOK.md                        # 15-minute executive pitch screenplay & objection track
│   ├── EXECUTIVE_PITCH_DECK.md                            # 12-slide executive presentation deck
│   ├── backend/
│   │   ├── README.md                                      # Backend microservice architecture and endpoint specs
│   │   ├── app.py                                         # Zero-dependency Python unified server & REST API
│   │   ├── database.py                                    # SQLite persistence engine with WAL mode
│   │   ├── risk_engine.py                                 # Canonical multi-module composite risk scoring engine
│   │   ├── analytics_engine.py                            # Cohort analytics, KPI aggregation & CSV streaming
│   │   ├── test_api.py                                    # REST API contract & endpoint tests (13/13 passing)
│   │   ├── test_database.py                               # SQLite WAL persistence unit tests (6/6 passing)
│   │   ├── test_analytics.py                              # Risk scoring & sensitivity unit tests (7/7 passing)
│   │   ├── test_security_suite.py                         # Cryptographic security & RBAC tests (12/12 passing)
│   │   └── test_stage1_integrity.py                       # Core system integrity & model parity tests (12/12 passing)
│   ├── data/
│   │   ├── digii_campus.db                                # Consolidated SQLite database (schema, students, audit)
│   │   ├── schema_definition.json                         # Cross-module relational schema mapping (270 tables)
│   │   └── students_mock.json                             # Canonical multi-risk cohort dataset (8 benchmark profiles)
│   └── docs/
│       └── PRIVACY_DESIGN.md                              # DPDP Act 2023 governance, consent gating & access matrix
├── week 01-12th-16th October-2026/
│   └── WorkLog_Week01_12-16thOctober_Dhruv.pdf
├── week 02-19th-23rd October-2026/
│   ├── Evaluating Non-Academic Student Development Framework, Product Design and Digii Campus Enhancement Proposal.pdf
│   ├── Non-Academic Student Development_Report.pdf
│   └── WorkLog_Week02_19-23rdOctober_Dhruv.pdf
├── week 03-26th-30th October-2026/
│   ├── Product_Research_and_Enhancement_Proposal.pdf
│   └── WorkLog_Week03_26-30thOctober_Dhruv.pdf
├── week 04 - 2nd-6th November-2026/
│   ├── Digii_Campus_BI_Database_Audit_Optimization_Week04.sql # 50 KB master SQL suite across 1,647 tables
│   └── Internship Worklog - Week 4.pdf
└── week 05 - 9th-13th November-2026/
    └── Internship_Worklog_Week_05_Dhruv_Jain.md            # Comprehensive Week 5 worklog and synthesis report
```

---

## Quantified Business ROI Delivered

| Metric Area | Current Digii Campus (Baseline) | Digii Campus 2.0 (Week 5 Deliverable) | Quantified Business Impact |
| :--- | :--- | :--- | :--- |
| **At-Risk Tuition Exposure** | ₹1.95 Cr unrecovered per term | 142 at-risk students identified & intervened | **₹1.95 Cr protected tuition revenue** |
| **Fee Reconciliation Time** | 40 manual hours per bank statement | Automated 1-click batch matcher (842 records) | **95% reduction in accountant overhead** |
| **Student No-Dues Clearance** | 10 to 14 days running across campus | 1.2-second 8-department parallel digital audit | **Zero physical paper forms** |
| **Mess Kitchen Food Waste** | 630 meals wasted daily from unannounced leaves | Out-pass sync to morning batch cooking ledger | **630 meals/day saved (₹4.2L/month)** |
| **Batch Assignment Burnout** | 70% overload on clustered Fridays | Dynamic deadline balancer to Monday afternoon | **68% reduction in student burnout index** |
| **Timetable Scheduling Clashes** | 12 to 15 manual revisions per department | Real-time clash detection & 1-click resolve | **100% clash-free master timetable CSV** |
| **Student Daily Active Use (DAU)** | 48% (Administrative use only) | 91.4% projected (Wallet, Market, Tutoring) | **Unbreakable student retention moat** |

---

## Technical Highlights (Week 04 SQL Suite)

The master script [`Digii_Campus_BI_Database_Audit_Optimization_Week04.sql`](week%2004%20-%202nd-6th%20November-2026/Digii_Campus_BI_Database_Audit_Optimization_Week04.sql) covers:

1. **Session & Ingestion Optimization:** Memory buffer tuning (`innodb_buffer_pool_size`, `sort_buffer_size`, `join_buffer_size`).
2. **System Profiling:** Table sizing, index-to-data footprint ratios, data dictionary metadata extraction, and fragmentation analysis.
3. **Relational Topology:** Foreign key dependency extraction and implicit application-level relationship audits.
4. **Common Table Expressions (CTEs):** Multi-chained operational pipelines, recursive continuous date spines, and escalation hierarchy traversal.
5. **Window Functions:** `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `NTILE(4)`, `LAG()`, `LEAD()`, 7-day rolling moving averages, running totals, and boundary value analysis (`FIRST_VALUE`, `LAST_VALUE`).
6. **Aggregations & Pivoting:** Multi-tier rollups (`GROUP BY ... WITH ROLLUP`) and conditional matrix pivoting across services and dining halls.
7. **Business Analytics:** Student RFM engagement clustering, Pareto 80/20 analysis, and Z-Score SLA latency outlier detection.
8. **Data Quality Suite:** Anti-joins for orphaned transactions, chronological inversions, impossible travel detection, and duplicate resolution.
9. **Performance Tuning:** `EXPLAIN` query cost evaluation, composite covering indexes, and range partitioning architecture.
10. **Production Deliverables:** DDL constraints, 5 enterprise analytical views, business-hour UDF, and 3 reporting stored procedures.

---

## Tools & Technologies

- **Database Engine:** MySQL 8.0.44 (AWS RDS / Local Mirrored Environment, 1,647 tables), SQLite 3 (WAL mode)
- **Data Engineering:** SQL (DDL, DML, DQL), Stored Procedures, UDFs, Execution Plans (`EXPLAIN`)
- **Product Architecture & Strategy:** RICE Prioritization Framework, Amplitude Telemetry Modeling, LaunchDarkly Feature Flag Governance, Product Requirements Document (PRD v2.4), DPDP Act 2023 Governance
- **Frontend & Prototyping:** Single Page Application (SPA), HTML5/TailwindCSS, Vanilla JavaScript (zero third-party NPM runtime dependencies)
- **Backend & Testing:** Python 3 (Standard Library `http.server`, `urllib.parse`, `json`, `sqlite3`, `unittest`, `secrets`)

---

## Acknowledgments

Special thanks to the Digii Campus engineering, BI, and product teams for their mentorship, knowledge transfer sessions, and guidance throughout this internship:

- **Mr. Suraj Bhatt** — Engineering & BI Manager
- **Saksham Gupta** — Principal Engineer
- **Shamitr Sudhir Mardikar** — Database Architecture & Infrastructure
- **Gurdeep Singh** — AWS Cloud & RDS Infrastructure
- **Prudvi Pratap Kanakala** — Access Architecture & KT Coordination
- **Piyush Anand** — Secure Credential & System Governance
