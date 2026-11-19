# Digii Campus 2.0 — Privacy by Design & Data Protection Specification
## Architectural Framework under India's Digital Personal Data Protection (DPDP) Act, 2023

---

### Executive Summary & Regulatory Grounding
This document establishes the official privacy, consent, and data protection architecture for the **Digii Campus 2.0 Proactive Retention & Student Intelligence System**. 

Previous drafts referenced foreign statutory frameworks (US FERPA, US HIPAA, EU GDPR, and ISO/IEC 27001). For Indian higher educational institutions deploying Digii Campus (CollPoll ERP), the binding legal standard is **India's Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)**. This document grounds all data ingestion, heuristic scoring, access control, and intervention dispatching under statutory DPDP principles.

---

### 1. Legal Roles & Definitions (DPDP Act 2023)
* **Data Fiduciary (Section 2(i))**: The University or Higher Educational Institution licensed to use Digii Campus ERP. Determines the purpose and means of student data processing.
* **Data Processor (Section 2(k))**: Digii Campus (CollPoll) as the multi-tenant SaaS cloud provider processing digital personal data on behalf of the Data Fiduciary.
* **Data Principal (Section 2(j))**: The enrolled student. Under Indian law (Indian Majority Act, 1875), students aged 18 and older are legal adults entitled to independent privacy protections.
* **Consent Manager (Section 6(7))**: Institutional registry managing verifiable digital consents, revocations, and communication preferences.

---

### 2. Signal Visibility Matrix (Role-Based Access Control)
In compliance with the principle of **Purpose Limitation (Section 4)** and **Data Minimization (Section 6)**, cross-module data signals are strictly segregated by institutional persona. No single operator possesses un-audited, blanket visibility into student records across domains.

| Module Signal / Data Field | Underlying Production Table | Super Administrator | Academic HOD / Dean | Hostel Warden | Finance Officer | Campus Help Centre Officer |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Attendance % & Missed Exams** | `classroom_attendance`, `course` | Read (Aggregate) | **Full Read / Write** | Denied | Denied | Denied |
| **Fee Installments & Overdue Dues** | `dues_v2`, `fee_collection` | Read (Aggregate) | Denied | Denied | **Full Read / Write** | Denied |
| **Turnstile & Curfew Logs** | `gate_pass_log`, `turnstile_telemetry` | Read (Aggregate) | Denied | **Full Read / Write** | Denied | Denied |
| **CHC Helpdesk Escalations** | `chc_request`, `chc_work_centre` | Read (Aggregate) | Denied | Denied | Denied | **Full Read / Write** |
| **Composite Retention Score (CRS)** | Derived Synthetic Engine | Read (Tiers) | Read (Academic Subscore) | Read (Hostel Subscore) | Read (Dues Subscore) | Read (Service Subscore) |
| **Action Center Dispatch** | `collpoll_audit_trail` | Audited | Departmental | Ward Only | Financial Clearance | Service Tickets |

---

### 3. Consent & Opt-In Architecture

#### 3.1 Tier-1 Notice & Affirmative Consent (Section 5)
1. **Notice on Enrollment**: Prior to ingesting attendance, turnstile, or dues data into predictive heuristic models, the Data Principal is presented with an itemized digital notice stating:
   * The specific data points processed (`dues_v2`, `classroom_attendance`, `gate_pass_log`, `chc_request`).
   * The purpose: Early academic intervention, bursar counseling, and institutional attrition mitigation.
   * The technical means: Rule-based heuristic scoring (not automated profiling without human review).
2. **Right to Withdraw Consent (Section 6(4))**: Students may opt out of automated early-warning telemetry via the Student Portal. Opting out disables algorithmic retention scoring without impacting core ERP functionality (course registration, hostel room allotment, or grade viewing).

#### 3.2 Adult Student Protection & "Summon Guardian" Consent Gating
* **Statutory Requirement**: Because college students are legal adults (18+), disclosing academic deficiency, financial status, or behavioral telemetry to parents/guardians without consent violates Section 6 of the DPDP Act.
* **Gated Workflow for `GUARDIAN` Summons**:
  1. The "Summon Guardian" action in the Action Center is **consent-gated** in the UI.
  2. The dispatching operator must affirmatively certify that valid guardian communication consent is on file (e.g. executed via university enrollment undertaking or academic probation standing agreement).
  3. All `GUARDIAN` actions are flagged with `legal_review_flagged: true` and dispatched to the Office of the Registrar and Institutional Legal Counsel for compliance review.
  4. Notice is logged with monotonic ID `AUD-xxxxxx` and recorded in the immutable audit trail.

---

### 4. Data Minimization & Non-Medical Grounding
* **Elimination of Health/Distress Telemetry**: In compliance with data minimization, the Campus Help Centre (CHC) signal is strictly restricted to administrative service requests, work centre dispatching, and infrastructure grievances (`chc_request`, `chc_work_centre`).
* **No Psychological Profiling**: Digii Campus 2.0 does not infer mental health, psychiatric states, or medical vulnerability. Clinical records remain segregated within medical infirmary records and are completely absent from the retention engine schema.

---

### 5. Data Retention & Erasure Schedule (Section 8(7))
1. **Raw Turnstile & Gate Logs**: Purged from operational retention indexes after 90 days. Aggregated to monthly breach counts in `access_gate_telemetry`.
2. **Predictive Composite Scores**: Recalculated dynamically; historical snapshots retained only for the duration of the active academic year.
3. **Graduation & "No-Dues" Clearance**: Upon completion of graduation clearance, all active predictive flags are permanently erased from retention tables; archive retained strictly for statutory degree audit.

---

### 6. Monotonic Immutable Audit Trail (Section 8(5))
Every interaction with student retention dossiers is tracked in the immutable `collpoll_audit_trail`:
* **Monotonic Sequence**: Monotonically incrementing identifiers (`AUD-000101`, `AUD-000102`, ...) prevent deletion or silent dropping of audit records.
* **Mandatory Metadata**: Each audit log records Operator UKID, Target Student UKID, Exact Action Type, Sanitized Text Notes, Timestamp (UTC), and Delivery Status.
* **Zero Race Conditions**: Thread-safe locking (`threading.Lock()`) ensures audit trail integrity under concurrent multi-user load.

---

### 7. Synthetic Data & Pitch Demo Transparency Banner
During local demonstration, technical pitch, or evaluative deployment:
* A permanent header banner is rendered across all views stating:
  > *"Simulated Enterprise Cohort & Simulated Actions: Synthetic dataset modeled on 10.08 GB MySQL replica distributions under India's Digital Personal Data Protection (DPDP) Act 2023. No live student PII. All intervention dispatches and financial clearance triggers are simulated prototypes for product architecture review."*

