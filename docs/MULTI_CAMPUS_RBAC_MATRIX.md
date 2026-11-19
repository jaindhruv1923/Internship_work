# Digii Campus 2.0 / CollPoll: Multi-Campus Role-Based Access Control (RBAC) Specification

## 1. Governance Architecture

In multi-institution deployments of CollPoll / Digii Campus, system security requires clear separation between institutional administration, academic instruction, student welfare, and self-service student/parent portals.

This document formalizes the 5-tier access control matrix, data partition rules, and row-level security (RLS) policies implemented across the 40 SPA views and underlying MySQL 8 database schema.

---

## 2. Institutional Role Hierarchy & Scope Boundaries

```
[ Tier 1: System Super Administrator / Chancellor ]
       │
       ▼
[ Tier 2: University Dean / Registrar / Finance Director ]
       │
       ▼
[ Tier 3: Department Head (HOD) / Program Coordinator ]
       │
       ▼
[ Tier 4: Course Faculty / Student Academic Mentor ]
       │
       ▼
[ Tier 5: Student / Parent Persona ]
```

---

## 3. Granular Permission Matrix by Module

| System Module / Capability | Tier 1 (Super Admin) | Tier 2 (Dean/Reg) | Tier 3 (HOD) | Tier 4 (Faculty) | Tier 5 (Student) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Institution Global Settings & DPDP Consent Vault** | Full Read/Write | Read Only | No Access | No Access | Self Consent Only |
| **Cohort Dropout Risk Overview (Aggregated CRS)** | Full View | Campus Scope | Dept Scope | Section Scope | Hidden (Only Advice) |
| **Student Detailed Risk Vector Inspection** | Audit Logged | Full View | Dept Scope | Assigned Mentee | Self Status Only |
| **Financial Arrears & Fee Payment Ledger** | Full Read/Write | Campus Scope | No Access | No Access | Self Invoice Only |
| **Attendance Ingestion & Biometric Overrides** | Full Audit | Read Only | Dept Override | Section Mark | Self View Only |
| **Continuous Internal Evaluation (CIE) Marks** | System Audit | Campus Audit | Dept Audit | Section Grade | Self View Only |
| **Predictive Intervention Logging & Counseling** | View All | View All | Dept Review | Create / Edit | Read Assigned Action |

---

## 4. Row-Level Security (RLS) SQL Implementation Strategy

In high-concurrency environments, application-layer filtering is fortified with database row-level security views:

```sql
-- Faculty View Filter: Restricts queries to active enrolled sections
CREATE OR REPLACE VIEW view_faculty_student_risk AS
SELECT 
    s.student_id,
    s.student_name,
    s.department_id,
    e.course_id,
    r.composite_risk_score,
    r.risk_tier,
    r.attendance_deficit_score
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id
INNER JOIN risk_scores r ON s.student_id = r.student_id
WHERE c.faculty_id = CURRENT_USER_FACULTY_ID()
  AND e.academic_term = CURRENT_ACADEMIC_TERM();
```

---

## 5. Session Token Security & Audit Logs

1. **JWT Scope Enforcement:** Tokens carry signed claims `institution_id`, `campus_id`, `role_tier`, and `department_id`.
2. **Deterministic Session Expiry:** 15-minute sliding session window with strict refresh rotation.
3. **Audit Trail Logging:** All access attempts to Tier 1 risk flags generate immutable audit entries signed with SHA-256 digests.
