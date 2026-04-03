"""
grader.py — Deterministic grader for the Legal Contract Review environment.
FIXED: Matching is now lenient — section + flag_type match is sufficient
       (agent doesn't need to guess exact manifest clause_id values).
"""
from __future__ import annotations
from typing import List, Tuple
from src.models import AgentFlag, FaultEntry, GraderResult


def grade_episode(
    agent_flags: List[AgentFlag],
    fault_manifest: List[FaultEntry],
) -> Tuple[GraderResult, float]:
    """
    Score an agent's flags against the ground-truth fault manifest.

    Returns (GraderResult, cumulative_reward).

    FIX: A flag is a True Positive if it matches ANY unmatched real fault in
    the same section with the same broad fault type (risky/missing).
    The agent does NOT need to supply the exact manifest clause_id.
    """
    real_faults = [f for f in fault_manifest if not f.is_trap]
    trap_faults = [f for f in fault_manifest if f.is_trap]

    true_positives   = 0
    false_positives  = 0
    missed_criticals = 0
    cumulative_reward = 0.0

    matched_fault_ids: set = set()

    for flag in agent_flags:
        matched = False

        for fault in real_faults:
            if fault.fault_id in matched_fault_ids:
                continue

            section_match = (flag.section == fault.section)

            # Broad type match: "risky" covers risky_clause, "missing" covers missing_clause
            type_match = (
                (flag.flag_type == "risky"   and fault.fault_type == "risky_clause") or
                (flag.flag_type == "missing" and fault.fault_type == "missing_clause")
            )

            # Exact clause_id match is a bonus but NOT required
            clause_id_exact = (flag.clause_id == fault.clause_id)

            # PRIMARY match rule: section + type (lenient)
            # SECONDARY: also allow section + exact clause_id regardless of type string
            if section_match and (type_match or clause_id_exact):
                true_positives += 1
                matched_fault_ids.add(fault.fault_id)
                matched = True

                # Base reward by severity
                if fault.risk_level == "critical":
                    cumulative_reward += 0.8
                elif fault.risk_level == "medium":
                    cumulative_reward += 0.6
                else:
                    cumulative_reward += 0.4

                # Bonus: correct risk_level
                if flag.risk_level == fault.risk_level:
                    cumulative_reward += 0.1

                # Bonus: redline submitted + standard language exists
                if flag.redline_suggested and fault.standard_language:
                    cumulative_reward += 0.3

                break  # each agent flag can match at most one fault

        if not matched:
            # Check if it accidentally hit a trap clause
            is_trap_flag = any(
                t.section == flag.section and (
                    t.clause_id == flag.clause_id or
                    # trap in same section with same type also counts
                    ((flag.flag_type == "risky"   and t.fault_type == "risky_clause") or
                     (flag.flag_type == "missing" and t.fault_type == "missing_clause"))
                )
                for t in trap_faults
            )
            false_positives += 1
            cumulative_reward -= 0.4
            if is_trap_flag:
                cumulative_reward -= 0.2  # extra trap penalty

    # Penalty for every unmatched critical fault
    for fault in real_faults:
        if fault.fault_id not in matched_fault_ids and fault.risk_level == "critical":
            missed_criticals += 1
            cumulative_reward -= 1.0

    # Score: F1-like, recall-weighted, with critical-miss penalty
    n_real    = len(real_faults)
    recall    = true_positives / n_real if n_real > 0 else 0.0
    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0.0
    )

    if (recall + precision) > 0:
        f_score = (2 * recall * precision) / (recall + precision)
    else:
        f_score = 0.0

    critical_penalty = 0.3 * missed_criticals / max(1, n_real)
    final_score = max(0.0, min(1.0, f_score - critical_penalty))

    return (
        GraderResult(
            true_positives=true_positives,
            false_positives=false_positives,
            missed_criticals=missed_criticals,
            score=round(final_score, 4),
        ),
        round(cumulative_reward, 4),
    )