# Digii Campus (CollPoll) — Data & Product Internship Worklogs

**Author:** Dhruv Jain  
**Role:** Data & Product Intern  
**Repository:** [github.com/jaindhruv1923/Internship_work](https://github.com/jaindhruv1923/Internship_work)  
**Reporting Period:** October – November 2026  

---

## Overview

This repository documents the work, research deliverables, and technical artifacts produced during my internship at **Digii Campus (formerly CollPoll)**. Over the course of the internship, the scope transitioned from frontend product research and non-academic development frameworks to backend enterprise data engineering, database administration, and large-scale Business Intelligence (BI) analytics.

The key focus of this repository is maintaining a transparent, reproducible record of weekly milestones, audit findings, analytical models, and production-grade SQL scripts.

---

## Weekly Progression

### Week 01: Onboarding, Architecture Alignment & Access Protocols
- **Period:** 12 October 2026 – 16 October 2026
- **Deliverables:**
  - `WorkLog_Week01_12-16thOctober_Dhruv.pdf`
- **Core Focus:**
  - Integrated into the Digii Campus engineering and product teams.
  - Explored core frontend modules and student life cycle workflows.
  - Reviewed enterprise security policies and operational compliance guidelines.

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
  - `Digii_Campus_BI_Database_Audit_Optimization_Week04.sql`
- **Core Focus:**
  - **Environment Configuration & 10GB Dump Ingestion:** Configured local MySQL 8.0 mirror environment to replicate AWS RDS production parameters. Resolved import bottlenecks (buffer pool sizing, `max_allowed_packet = 1GB`, query timeout tuning).
  - **Comprehensive Schema Exploration (1,647 Tables):** Categorized all tables across 15 enterprise architectural domains (EMS, Identity/Auth, CHC Service Desk, Finance/Dues, Hostel, Turnstile Access, Mess/Dining, etc.).
  - **Relational Reverse-Engineering:** Mapped primary/foreign key graphs and audited soft/implicit relationships across core modules.
  - **Data Quality Audit & Anomaly Detection:** Formulated queries isolating historical data anomalies, including orphaned transactional logs, chronological window inversions (`pass_end < pass_start`), impossible travel (<180s multi-gate punches), and hostel attendance vs gate exit discrepancies.
  - **Advanced Analytical SQL:** Implemented recursive CTEs (dynamic 90-day calendar date spine, escalation hierarchy traversal), window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE(4)`, `LAG`/`LEAD`, rolling 7-day moving averages, cumulative sums), multidimensional rollups, and conditional matrix pivots.
  - **Quantitative Business Analytics:** Built an RFM (Recency, Frequency, Intensity) student engagement scoring model, Pareto (80/20) escalation root-cause analysis, and Z-Score outlier detection for ticket resolution turnaround times.
  - **Production Enhancements:** Engineered composite/covering indexes, structural DDL `CHECK` constraints, 5 enterprise analytical BI views, a business-hour calculation UDF, and 3 automated reporting stored procedures aligned with the ClickUp 5-step workflow.

---

## Repository Structure

```
.
├── .gitignore
├── README.md
├── product_enhancement/
│   ├── PRD_Proactive_Retention_System.md
│   ├── index.html
│   ├── package.json
│   ├── server.ps1
│   ├── backend/
│   │   ├── README.md
│   │   ├── app.py
│   │   └── test_api.py
│   └── data/
│       ├── schema_definition.json
│       └── students_mock.json
├── week 01-12th-16th October-2026/
│   └── WorkLog_Week01_12-16thOctober_Dhruv.pdf
├── week 02-19th-23rd October-2026/
│   ├── Evaluating Non-Academic Student Development Framework, Product Design and Digii Campus Enhancement Proposal.pdf
│   ├── Non-Academic Student Development_Report.pdf
│   └── WorkLog_Week02_19-23rdOctober_Dhruv.pdf
├── week 03-26th-30th October-2026/
│   ├── Product_Research_and_Enhancement_Proposal.pdf
│   └── WorkLog_Week03_26-30thOctober_Dhruv.pdf
└── week 04 - 2nd-6th November-2026/
    ├── Digii_Campus_BI_Database_Audit_Optimization_Week04.sql
    └── Internship Worklog - Week 4.pdf
```

---

## Featured Product Enhancement: Proactive Student Retention System (BI Portal 2.0)

As a proactive capstone bridging the 10.08 GB production database audit with enterprise product management, I designed and built an interactive working prototype of **Digii Campus BI Portal 2.0: Proactive Student Retention & Intelligence System** located in [`product_enhancement/`](product_enhancement/).

### Key Capabilities:
1. **Predictive Student Dropout Radar:** Analyzes cross-module operational signals (academics, fees, turnstiles, residential curfews, health visits) to compute a compound risk score (0–100) flagging students in distress weeks before formal administrative failure.
2. **Student 360 Unified Timeline:** Replaces 5 fragmented ERP tabs with a single, chronological activity feed giving Deans and HODs full context in under 15 seconds.
3. **1-Click Intervention Action Center:** Integrated, pre-composed multi-channel actions (`Automated Nudge Email`, `Escalate to HOD`, `Schedule Counseling`, `Summon Guardian`) directly closing the loop between data insight and student retention.
4. **Dynamic Heuristics & Sensitivity Tuner (Phase 4):** Live multi-domain weight sliders allowing administrators to simulate risk sensitivity across all 4,850 students with real-time recalculation.
5. **Behind the Data — SQL Lineage Inspector (Phase 4):** Exposes production MySQL queries from the Week 4 10.08 GB audit (CTEs, window functions, and cross-module joins).
6. **Administrative Intervention Audit Trail (Phase 4):** Immutable, timestamped audit log table tracking every dispatched institutional action for ISO 27001/FERPA compliance.
7. **Zero-Dependency Python REST Microservice (Phase 4):** Standard-library Python backend with full REST API, CSV streaming, and automated test suite with 100% pass rate (`backend/app.py` & `backend/test_api.py`).
8. **Comprehensive PRD:** Enterprise-grade Product Requirements Document detailing user personas, heuristic weighting formulas, and phased delivery roadmap ([`PRD_Proactive_Retention_System.md`](product_enhancement/PRD_Proactive_Retention_System.md)).

To run the local prototype (Frontend):
```powershell
powershell -ExecutionPolicy Bypass -File .\product_enhancement\server.ps1 -Port 3000
# Open http://localhost:3000 in your browser
```

To run the Python REST API backend and test suite:
```powershell
# Run backend microservice
python .\product_enhancement\backend\app.py 8000

# Run automated unit test suite
python .\product_enhancement\backend\test_api.py
```

> **Note on Database Replica Dump:**  
> The 10.08 GB production-replica database dump (`bi_dump_2026_05_08_updated.sql`) evaluated during Week 4 is hosted on internal infrastructure and excluded from this repository via `.gitignore` in compliance with enterprise data security policies and GitHub file size limitations.

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

- **Database Engine:** MySQL 8.0.44 (AWS RDS / Local Mirrored Environment)
- **Data Engineering:** SQL (DDL, DML, DQL), Stored Procedures, UDFs, Execution Plans (`EXPLAIN`)
- **Product Design & Research:** Figma, Product Requirement Documentation (PRD), Workflow Mapping
- **Project Management & Compliance:** ClickUp, Enterprise 5-Step Access Policy

---

## Acknowledgments

Special thanks to the Digii Campus engineering, BI, and product teams for their mentorship, knowledge transfer sessions, and guidance throughout this internship:
- **Mr. Suraj Bhatt** — Engineering & BI Manager
- **Shamitr Sudhir Mardikar** — Database Architecture & Infrastructure
- **Gurdeep Singh** — AWS Cloud & RDS Infrastructure
- **Prudvi Pratap Kanakala** — Access Architecture & KT Coordination
- **Piyush Anand** — Secure Credential & System Governance
