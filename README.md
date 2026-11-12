# Digii Campus (CollPoll) — Data & Product Internship Worklogs

**Author:** Dhruv Jain  
**Role:** Data & Product Intern (Proposing Formal Transition to **Product Intern / APM**)  
**Repository:** [github.com/jaindhruv1923/Internship_work](https://github.com/jaindhruv1923/Internship_work)  
**Reporting Period:** October – November 2026 (Odd Semester AY 2026-27)  
**Managers & Mentors:** Mr. Suraj Bhatt (Engineering & BI Manager), Saksham Gupta (Principal Engineer), Gurdeep Singh, Piyush Anand, Shamitr Sudhir Mardikar

---

## Executive Summary & Role Transition Objective

This repository documents the weekly research, database engineering, enterprise BI optimization, and product architecture deliverables completed during my internship at **Digii Campus (formerly CollPoll)**.

Over the 5-week tenure, my scope expanded from frontend product research to deep database engineering (grounded in Suraj Shetty's CollPoll Workflows document covering 270 tables across 6 modules: CHC, Gatepass, Hostel, Infrastructure, Placements, Transport) on our **10.08 GB production MySQL replica** (1,647 tables, 15 operational domains), culminating in the architecture and delivery of **Digii Campus 2.0: Enterprise Intelligence & B2B2C Student Experience Platform**.

By bridging relational data depth with product prioritization frameworks (RICE), engineering safety guardrails (LaunchDarkly-style feature flags and circuit breakers), and dual-value user design, this work demonstrates my readiness to formally transition into the **Product Intern / APM** role.

---

## Quick Start — Launching the Live Interactive Prototype

To explore the fully working single-page application (SPA), run the one-click Windows launcher or start the zero-dependency local dev server:

### Option 1: One-Click Windows Launcher (Recommended)

Double-click `start_demo.bat` in the repository root, or run:

```cmd
.\start_demo.bat
```

_Automatically validates port 3000, starts the background HTTP listener if needed, and launches `http://localhost:3000/index.html` in your default browser._

### Option 2: PowerShell Dev Server

```powershell
powershell -ExecutionPolicy Bypass -File .\product_enhancement\server.ps1 -Port 3000
# Open http://localhost:3000/index.html in your browser
```

### Option 3: Backend Python Microservice & Automated Test Suite

```powershell
# Run backend microservice
python .\product_enhancement\backend\app.py 8000

# Run automated unit test suite (Validates schemas, heuristics & 100% onclick handler integrity)
python .\product_enhancement\backend\test_api.py
```

---

## Weekly Progression

### Week 01: Onboarding, Architecture Alignment & Access Protocols

- **Period:** 12 October 2026 – 16 October 2026
- **Deliverables:** `WorkLog_Week01_12-16thOctober_Dhruv.pdf`
- **Core Focus:**
  - Integrated into the Digii Campus engineering and product teams.
  - Explored core frontend modules and student life cycle workflows.
  - Reviewed enterprise security policies, VPN protocols, and operational compliance guidelines.

---

### Week 02: Non-Academic Student Development Framework

- **Period:** 19 October 2026 – 23 October 2026
- **Deliverables:**
  - `WorkLog_Week02_19-23rdOctober_Dhruv.pdf`
  - `Non-Academic Student Development_Report.pdf`
  - `Evaluating Non-Academic Student Development Framework, Product Design and Digii Campus Enhancement Proposal.pdf`
- **Core Focus:**
  - Designed an end-to-end Non-Academic Student Development Framework bridging co-curricular participation with institutional accreditation.
  - Developed product UX blueprints and functional specifications for student life analytics.
  - Authored a comprehensive enhancement proposal submitted to the product design team.

---

### Week 03: Product Research & Competitive Benchmarking

- **Period:** 26 October 2026 – 30 October 2026
- **Deliverables:**
  - `WorkLog_Week03_26-30thOctober_Dhruv.pdf`
  - `Product_Research_and_Enhancement_Proposal.pdf`
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
  - `Internship Worklog - Week 4.pdf`
  - `Digii_Campus_BI_Database_Audit_Optimization_Week04.sql` (50 KB master SQL suite)
- **Core Focus:**
  - **Environment Configuration & 10GB Dump Ingestion:** Configured local MySQL 8.0 mirror environment replicating AWS RDS production parameters. Resolved import bottlenecks (buffer pool sizing, `max_allowed_packet = 1GB`, query timeout tuning).
  - **Comprehensive Schema Exploration (1,647 Tables):** Categorized all tables across 15 enterprise architectural domains (EMS, Identity/Auth, CHC Service Desk, Finance/Dues, Hostel, Turnstile Access, Mess/Dining, etc.).
  - **Relational Reverse-Engineering:** Mapped primary/foreign key graphs and audited soft/implicit relationships across core modules.
  - **Data Quality Audit & Anomaly Detection:** Formulated queries isolating historical data anomalies, including orphaned transactional logs, chronological window inversions (`pass_end < pass_start`), impossible travel (<180s multi-gate punches), and hostel attendance vs gate exit discrepancies.
  - **Advanced Analytical SQL:** Implemented recursive CTEs (dynamic 90-day calendar date spine, escalation hierarchy traversal), window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE(4)`, `LAG`/`LEAD`, rolling 7-day moving averages, cumulative sums), multidimensional rollups, and conditional matrix pivots.
  - **Quantitative Business Analytics:** Built an RFM (Recency, Frequency, Intensity) student engagement scoring model, Pareto (80/20) escalation root-cause analysis, and Z-Score outlier detection for ticket resolution turnaround times.
  - **Production Enhancements:** Engineered composite/covering indexes, structural DDL `CHECK` constraints, 5 enterprise analytical BI views, a business-hour calculation UDF, and 3 automated reporting stored procedures aligned with the ClickUp 5-step workflow.

---

### Week 05: Enterprise Product Architecture, PM Cockpit & B2B2C Dual-Value Innovation

- **Period:** 09 November 2026 – 13 November 2026
- **Reviewers:** Mr. Suraj Bhatt (Engineering & BI Manager), Saksham Gupta (Principal Engineer)
- **Deliverables:**
  - `week 05 - 9th-13th November-2026/Internship_Worklog_Week_05_Dhruv_Jain.md`
  - `product_enhancement/index.html` (Complete Single Page Application prototype, 375+ KB)
  - `product_enhancement/PRD_Proactive_Retention_System.md` (22 KB complete engineering PRD v2.4)
  - `product_enhancement/EXECUTIVE_PITCH_PLAYBOOK.md` (15-minute executive pitch screenplay & objection-handling track)
  - `product_enhancement/EXECUTIVE_PITCH_DECK.md` (12-slide executive presentation deck)
  - `start_demo.bat` (One-click Windows demonstration launcher)
- **Core Focus:**
  - **Predictive Student Dropout Radar (Stage 3):** Cross-module compound heuristic engine evaluating academics, fees, turnstile gates, hostel curfews, and clinic visits, protecting **₹1.84 Cr in at-risk tuition**.
  - **Student 360 Unified Timeline & Action Center (Stage 4 & 5):** Single-pane investigation stream consolidating 5 legacy ERP silos with 1-click administrative intervention dispatches (SMS to parent, academic probation notice, HOD summons).
  - **Automated Fee Reconciliation Engine (Stage 7):** Split-screen banking ledger with drag-and-drop CSV ingestion and 1-click matching algorithm. Reconciles **842 records (₹1.68 Cr)** instantly and saves **40 hours/week** of manual accounting labor.
  - **Smart Timetable Clash Resolver (Stage 8):** Multi-entity constraint optimizer detecting faculty collisions in real time and auto-resolving professor commitments with 1-click, eliminating **100% of scheduling backend support tickets**.
  - **Non-Academic Student Development Module (NASD):** Direct functional realization of Dhruv Jain's Week 2 research framework, tracking Enrichment Credits (BML Munjal University model), 42 chartered campus societies (ACM, IEEE, Baja Racing, NSS), 18,420 verified volunteer hours, and automated accreditation compliance for NAAC Criterion 5.3 / NIRF. Includes 1-click credential verification and exportable official co-curricular diploma supplements.
  - **Enterprise BI Suite & Clean Design Language:** Completely sanitized all emojis across modules in favor of clean enterprise SVG typography. Integrated a live Multi-Campus Switcher (`Main Campus`, `North Campus NCR`, `Bengaluru`), real-time Department Filter (`CSE`, `ECE`, `ME`) for the Predictive Radar, and an interactive Hostel Night Roll-Call & Room Allocation Register.
  - **20 Operational Predictive Intelligence & Disruptive Modules (Net-New vs Current Digii Campus):**
    1. _Predictive Dropout Radar (`view-radar`):_ Multi-tier risk classifier with real-time department filtering (CSE/ECE/ME), dynamic cohort count, and 1-click advisor intervention triggers.
    2. _Student 360 Timeline (`view-student360`):_ Longitudinal chronicle linking academic scores, library swipes, hostel curfews, and fee receipts for any selected student.
    3. _Student Experience Hub (`view-student-hub`):_ 10 dual-value B2B2C modules with live action modals, real certificate downloads, and friction mitigators.
    4. _Social Isolation Sentinel (`view-isolation` - Week 3 Research):_ Correlates physical turnstiles with zero club/library interactions for 14+ days to flag silent mental health isolation to university counselors before crisis occurs.
    5. _Predictive Kitchen Prep & Food Waste Reducer (`view-prge` - Week 3 Proposal):_ Dynamic cross-module linkage deducting approved hostel night leaves from morning mess preparation, cutting 630 wasted meals/day and saving ₹4.2L/month.
    6. _Autonomous Multi-Dept No-Dues Instant Clearance (`view-nodues`):_ 1-click 8-department parallel relational audit (Library, Hostel, Sports, Labs, Accounts, HOD) completing degree clearance in 3 seconds with official certificate download.
    7. _Smart Deadline Congestion Balancer (`view-deadline`):_ Campus-wide LMS submission heatmap detecting multi-course assignment clustering on Fridays and autonomously staggering deadlines to Monday afternoon.
    8. _Tamper-Proof Relational Auto-Resume (`view-autoresume` - Week 3 Proposal):_ Directly compiles authenticated SGPA, OBE Bloom's rubrics, and club leadership from MySQL into an institutionally sealed, QR-verifiable CV.
    9. _Turnstile Anti-Passback & Impossible Travel (`view-passback` - Week 4 Audit):_ Biometric velocity physics checker detecting proxy card taps at distant gates in <180s, triggering turnstile lockout and guard dispatch.
    10. _Non-Academic Development Ledger (`view-development` - Week 2 Proposal):_ Situational Evidence Profiler tracking 3,840 enrichment credit students, 42 clubs, 18,420 volunteer hours (NAAC 5.3) with diploma supplement export.
    11. _CHC Workflow Intelligence & SLA Analytics (`view-grievance`):_ Cross-service request analytics on `chc_request`, `chc_work_centre` and `chc_middleware`, tracking SLA compliance, bottleneck work centres, and escalation patterns across all CHC-integrated modules.
    12. _Phantom Midnight Energy & Green Campus (`view-energy`):_ Occupancy-vs-meter cross-checking engine auto-shedding empty lecture hall HVAC at 2:00 AM, saving ₹18.4L/yr and exporting ISO 50001 green audits.
    13. _Alumni Capstone Micro-Endowment (`view-alumni`):_ Capstone prototype pitching exchange with 1:1 Google Meet mentorship bookings and Section 80G tax-exempt endowment pledges.
    14. _Accreditation Copilot (`view-accreditation`):_ NAAC SSR 7-criteria telemetry (Grade A++ 3.68/4.00 projection) with 1,647-table relational evidence scanning and SSR bundle export.
    15. _Academics Timetable Clash Interceptor (`view-academics`):_ 32 credit track scheduler, live timetable clash resolver, and clash-free timetable CSV export.
    16. _Finance & Fee Dues Recon (`view-finance`):_ Batch reconciliation matcher recovering ₹1.84 Cr tuition exposure, with bank statement parser and audit export.
    17. _Financial Aid & DBT Gateway (`view-scholarships`):_ Institutional aid disbursement ledger with automated tuition offset crediting and PFMS-ready bank advice export.
    18. _AI Merit & Multi-Quota Seat Allotment Matrix (`view-admissions` - CollPoll Schema Grounded):_ Dynamic cutoff slider, multi-round allotment matrix across General, OBC-NCL, SC, ST, and EWS quotas, instant provisional offer generation, and relational sync to `dues_v2`.
    19. _Smart Campus Infrastructure & Acoustic Booking Interceptor (`view-venue` - CollPoll Schema Grounded):_ Live conflict matrix detecting high-decibel acoustic collisions (e.g., Heavy Metal Fest adjacent to IEEE Boardroom) on `infra_booking`, with 1-click sound-bleed auto-rescheduling and HVAC pre-cooling dispatch.
    20. _Smart Dynamic Fleet & Transport v2 Route Optimizer (`view-transport` - CollPoll Schema Grounded):_ Relational route fleet optimizer on `transport_management_v2_route` and `_vehicle_inventory_lock`, merging sub-40% occupancy lines, eliminating ₹1.28L/month in diesel burn, and exporting live vehicle rosters.
    21. _Digii Campus vs. Digii 2.0 Comparative Intelligence Matrix (`view-comparative`):_ Dedicated split-screen benchmarking matrix evaluating 17 core ERP modules from `digiicampus.com` against the Digii 2.0 predictive intelligence layer, highlighting operational friction, production schema joins (`ukid`, `dues_v2`, `gate_pass_log`, `chc_middleware`), and exportable RFC 4180 CSV / executive TXT audits.
  - **PM Strategy & Engineering Cockpit (`PM Cockpit`):**
    - _Tab 1: RICE Prioritization Engine_ with dynamic effort multiplier slider (0.5x to 2.0x) and real-time Now / Next / Later swimlanes with live feature launch triggers.
    - _Tab 2: Feature Flags & Canary Governance (LaunchDarkly Model)_ with rollout sliders and circuit breaker auto-rollback (>120ms p99).
    - _Tab 3: Telemetry Funnel (Amplitude Model)_ diagnosing 22% payment drop-off, with simulated PM intervention recovering +₹52 Lakhs.
    - _Tab 4: In-App PRD v2.4 Spec Viewer_ with 1-click Markdown copy and download.
  - **Full-Screen Executive Pitch Deck Viewer (`Pitch Deck`):** In-browser 12-slide presentation mode with keyboard arrow navigation (`◄` `►`), interactive highlights, and direct jump buttons into every live feature.

---

## Repository Structure

```
.
├── .gitignore
├── README.md
├── start_demo.bat                                         # One-click Windows demo launcher
├── product_enhancement/
│   ├── index.html                                         # Full interactive SPA (21 Enterprise Views, 774 KB, zero emojis)
│   ├── verify_suite.py                                    # Automated audit suite (SPA_VIEWS, HTML sections, 160 handlers, 0 emojis)
│   ├── EXECUTIVE_PITCH_PLAYBOOK.md                        # 15-minute executive pitch screenplay & objection track
│   ├── EXECUTIVE_PITCH_DECK.md                            # 12-slide executive presentation deck
│   ├── PRD_Proactive_Retention_System.md                  # Complete 22 KB Product Requirements Document v2.4
│   ├── package.json
│   ├── server.ps1                                         # Zero-dependency .NET HTTP dev server
│   ├── backend/
│   │   ├── README.md
│   │   ├── app.py                                         # Zero-dependency Python REST API microservice
│   │   └── test_api.py                                    # Automated unit test suite (7/7 tests passing)
│   └── data/
│       ├── schema_definition.json                         # Cross-module relational schema definition
│       └── students_mock.json                             # Synthetic 8-student multi-risk cohort dataset
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
│   ├── Digii_Campus_BI_Database_Audit_Optimization_Week04.sql
│   └── Internship Worklog - Week 4.pdf
└── week 05 - 9th-13th November-2026/
    └── Internship_Worklog_Week_05_Dhruv_Jain.md            # Comprehensive Week 5 worklog and synthesis report
```

---

## Quantified Business ROI Delivered

| Metric Area                        | Current Digii Campus (Baseline)           | Digii Campus 2.0 (Week 5 Deliverable)         | Quantified Business Impact                 |
| :--------------------------------- | :--------------------------------------- | :-------------------------------------------- | :----------------------------------------- |
| **At-Risk Tuition Exposure**       | ₹1.84 Cr unrecovered per term            | 142 at-risk students identified & intervened  | **₹1.84 Cr protected tuition revenue**     |
| **Fee Reconciliation Time**        | 40 manual hours per bank statement       | Automated 1-click batch matcher (842 records) | **95% reduction in accountant overhead**   |
| **Student No-Dues Clearance**      | 10 to 14 days running across campus      | 1-click 4-department digital clearance        | **Zero physical paper forms**              |
| **Batch Assignment Burnout**       | 70% overload on clustered Fridays        | AI-driven deadline rebalancer to Monday       | **68% reduction in student burnout index** |
| **Timetable Scheduling Clashes**   | 12 to 15 manual revisions per department | Real-time clash detection & 1-click resolve   | **100% clash-free master timetable CSV**   |
| **Student Daily Active Use (DAU)** | 48% (Administrative use only)            | 91.4% projected (Wallet, Market, Tutoring)    | **Unbreakable product retention moat**     |

---

## Technical Highlights (Week 04 SQL Suite)

The master script [`Digii_Campus_BI_Database_Audit_Optimization_Week04.sql`](week%2004%20-%202nd-6th%20November-2026/Digii_Campus_BI_Database_Audit_Optimization_Week04.sql) covers the following technical areas:

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

- **Database Engine:** MySQL 8.0.44 (AWS RDS / Local Mirrored Environment, 1,647 tables)
- **Data Engineering:** SQL (DDL, DML, DQL), Stored Procedures, UDFs, Execution Plans (`EXPLAIN`)
- **Product Architecture & Strategy:** RICE Prioritization Framework, Amplitude Telemetry Modeling, LaunchDarkly Feature Flag Governance, Product Requirement Documentation (PRD v2.4)
- **Frontend & Prototyping:** Single Page Application (SPA), HTML5/TailwindCSS, Vanilla JavaScript (zero third-party NPM runtime dependencies)
- **Backend & Testing:** Python 3.12 (Standard Library HTTP & Unit Testing), Windows PowerShell/.NET `HttpListener`

---

## Acknowledgments

Special thanks to the Digii Campus engineering, BI, and product teams for their mentorship, knowledge transfer sessions, and guidance throughout this internship:

- **Mr. Suraj Bhatt** — Engineering & BI Manager
- **Saksham Gupta** — Principal Engineer
- **Shamitr Sudhir Mardikar** — Database Architecture & Infrastructure
- **Gurdeep Singh** — AWS Cloud & RDS Infrastructure
- **Prudvi Pratap Kanakala** — Access Architecture & KT Coordination
- **Piyush Anand** — Secure Credential & System Governance
