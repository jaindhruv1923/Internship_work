#!/usr/bin/env python3
"""
Canonical Risk Engine for Digii Campus Proactive Retention System.
Single source of truth for composite risk calculation, weight validation, and threshold checking.
Both Python backend (app.py) and frontend (index.html) must adhere to this exact specification.
"""

# Default Heuristic Weights (Sum = 1.0)
import math

DEFAULT_WEIGHTS = {
    "academics": 0.35,
    "fees": 0.25,
    "gates": 0.15,
    "hostel": 0.15,
    "chc": 0.10
}

# Default Risk Tier Thresholds
DEFAULT_THRESHOLDS = {
    "red_zone": 75.0,
    "amber_zone": 50.0
}

def validate_weights(weights):
    """
    Validates that weights is a dictionary containing all required numeric keys,
    each between 0.0 and 1.0, and normalizing them if sum != 1.0.
    Returns (is_valid, normalized_weights, error_message).
    """
    if not isinstance(weights, dict):
        return False, None, "Weights must be a JSON object"

    required_keys = ["academics", "fees", "gates", "hostel", "chc"]
    cleaned = {}
    for k in required_keys:
        if k not in weights:
            return False, None, f"Missing weight key: {k}"
        try:
            val = float(weights[k])
        except (ValueError, TypeError):
            return False, None, f"Weight for {k} must be numeric"
        if val < 0.0 or val > 1.0:
            return False, None, f"Weight for {k} must be between 0.0 and 1.0 (received {val})"
        cleaned[k] = val

    total = sum(cleaned.values())
    if total <= 0.0:
        return False, None, "Total sum of weights must be greater than zero"

    # Normalize weights so they sum strictly to 1.0
    normalized = {k: round(v / total, 4) for k, v in cleaned.items()}
    # Adjust slight rounding difference onto academics
    diff = 1.0 - sum(normalized.values())
    if abs(diff) > 0.0:
        normalized["academics"] = round(normalized["academics"] + diff, 4)

    return True, normalized, None

def validate_thresholds(thresholds):
    """
    Validates that 0 <= amber_zone < red_zone <= 100.
    Returns (is_valid, cleaned_thresholds, error_message).
    """
    if not isinstance(thresholds, dict):
        return False, None, "Thresholds must be a JSON object"

    red = thresholds.get("red_zone", DEFAULT_THRESHOLDS["red_zone"])
    amber = thresholds.get("amber_zone", DEFAULT_THRESHOLDS["amber_zone"])

    try:
        red = float(red)
        amber = float(amber)
    except (ValueError, TypeError):
        return False, None, "Thresholds red_zone and amber_zone must be numeric"

    if red > 100.0 or red < 1.0:
        return False, None, "red_zone threshold must be between 1 and 100"
    if amber < 0.0 or amber >= red:
        return False, None, f"amber_zone threshold ({amber}) must be >= 0 and strictly less than red_zone ({red})"

    return True, {"red_zone": red, "amber_zone": amber}, None

def calculate_student_risk(student, weights=None, thresholds=None):
    """
    Calculates the single canonical Composite Risk Score (CRS) between 0 and 100
    for a given student record.
    """
    w = dict(weights) if weights else dict(DEFAULT_WEIGHTS)
    th = dict(thresholds) if thresholds else dict(DEFAULT_THRESHOLDS)

    # 1. Academic sub-score (0-100)
    att = float(student.get("academics", {}).get("overall_attendance_pct", 85.0))
    acad_score = max(0.0, min(100.0, (75.0 - att) * 4.0)) if att < 75.0 else 5.0
    missed_assessments = student.get("academics", {}).get("missed_assessments", [])
    if len(missed_assessments) > 0:
        acad_score = min(100.0, acad_score + 25.0)

    # 2. Finance sub-score (0-100)
    dpd = float(student.get("finance", {}).get("overdue_days", 0))
    dues = float(student.get("finance", {}).get("amount_overdue", 0))
    fin_score = 0.0
    if dues > 0:
        fin_score = min(100.0, (dpd / 45.0) * 75.0 + (min(dues, 150000.0) / 150000.0) * 25.0)

    # 3. Gate turnstile sub-score (0-100)
    gate_data = student.get("access_gate_telemetry", {})
    late_entries = float(gate_data.get("late_entries_30d", 0))
    missing_exits = float(gate_data.get("missing_exit_logs", 0))
    gate_evts = [e for e in student.get("timeline_events", []) if e.get("module") == "ACCESS_GATE"]
    gate_crit = sum(1 for e in gate_evts if e.get("severity") == "CRITICAL")
    gate_warn = sum(1 for e in gate_evts if e.get("severity") == "WARNING")
    gate_score = min(100.0, late_entries * 15.0 + missing_exits * 20.0 + gate_crit * 25.0 + gate_warn * 10.0)

    # 4. Hostel residential sub-score (0-100)
    is_hosteller = student.get("accommodation_type") == "HOSTELLER"
    curfews = float(gate_data.get("curfew_breaches_30d", 0))
    hostel_evts = [e for e in student.get("timeline_events", []) if e.get("module") == "HOSTEL"]
    hostel_crit = sum(1 for e in hostel_evts if e.get("severity") == "CRITICAL")
    hostel_warn = sum(1 for e in hostel_evts if e.get("severity") == "WARNING")
    if is_hosteller:
        hostel_score = min(100.0, curfews * 25.0 + hostel_crit * 40.0 + hostel_warn * 20.0)
    else:
        hostel_score = 0.0

    # 5. Campus Help Centre (CHC) service requests & SLA escalations (0-100)
    # Grounded strictly in chc_request and chc_work_centre workflow tables (no medical/psychological)
    chc_evts = [e for e in student.get("timeline_events", []) if e.get("module") in ("CHC", "CHC_REQUEST", "CAMPUS_HELP_CENTRE")]
    chc_crit = sum(1 for e in chc_evts if e.get("severity") == "CRITICAL")
    chc_warn = sum(1 for e in chc_evts if e.get("severity") == "WARNING")
    chc_info = sum(1 for e in chc_evts if e.get("severity") == "INFO")
    chc_score = min(100.0, chc_crit * 50.0 + chc_warn * 25.0 + chc_info * 10.0)

    # Weighted Sum strictly clamped to 0..100
    raw_total = (
        w["academics"] * acad_score +
        w["fees"] * fin_score +
        w["gates"] * gate_score +
        w["hostel"] * hostel_score +
        w["chc"] * chc_score
    )
    score_clamped = max(0.0, min(100.0, raw_total))
    score_int = int(math.floor(score_clamped + 0.5))

    # Tier Allocation based on validated thresholds
    red_th = th.get("red_zone", DEFAULT_THRESHOLDS["red_zone"])
    amber_th = th.get("amber_zone", DEFAULT_THRESHOLDS["amber_zone"])
    if score_int >= red_th:
        tier = "HIGH"
    elif score_int >= amber_th:
        tier = "MEDIUM"
    else:
        tier = "HEALTHY"

    return {
        "score": score_int,
        "tier": tier,
        "sub_scores": {
            "academics": math.floor(acad_score * 10 + 0.5) / 10.0,
            "fees": math.floor(fin_score * 10 + 0.5) / 10.0,
            "gates": math.floor(gate_score * 10 + 0.5) / 10.0,
            "hostel": math.floor(hostel_score * 10 + 0.5) / 10.0,
            "chc": math.floor(chc_score * 10 + 0.5) / 10.0
        }
    }

