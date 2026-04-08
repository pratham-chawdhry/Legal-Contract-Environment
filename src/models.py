"""
models.py — Typed Pydantic models for the Legal Contract Review environment.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ------------------------------------------------------------------ #
# Action
# ------------------------------------------------------------------ #

class ContractAction(BaseModel):
    action_type: str = Field(
        ...,
        description=(
            "One of: read_section, flag_clause, mark_missing, "
            "suggest_redline, approve_section, summarize"
        ),
    )
    params: Dict[str, Any] = Field(default_factory=dict)


# ------------------------------------------------------------------ #
# Observation sub-models
# ------------------------------------------------------------------ #

class SectionStatus(BaseModel):
    section_name: str
    read: bool
    approved: bool
    flags_count: int


class AgentFlag(BaseModel):
    section: str
    clause_id: str
    flag_type: str          # "risky" | "missing"
    risk_level: str         # "low" | "medium" | "critical"
    reason: str
    redline_suggested: bool = False


class GraderResult(BaseModel):
    true_positives: int
    false_positives: int
    missed_criticals: int
    score: float            # 0.0 – 1.0


# ------------------------------------------------------------------ #
# Observation
# ------------------------------------------------------------------ #

class ContractObservation(BaseModel):
    task_id: str
    difficulty: str
    description: str
    max_steps: int

    # Contract state
    contract_title: str
    available_sections: List[str]
    section_statuses: List[SectionStatus]
    current_section_text: Optional[str] = None
    current_section_name: Optional[str] = None

    # Agent progress
    flags: List[AgentFlag]
    actions_taken: List[str]
    last_action_result: str

    # Episode state
    step: int
    done: bool
    pipeline_passed: bool   # True when summarize() called with sufficient score

    # Grader hint (partial, not full manifest)
    total_faults_in_contract: int
    faults_found_so_far: int


# ------------------------------------------------------------------ #
# Reward / Step result
# ------------------------------------------------------------------ #

class StepResult(BaseModel):
    observation: ContractObservation
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)


# ------------------------------------------------------------------ #
# Internal fault manifest (not exposed to agent)
# ------------------------------------------------------------------ #

class FaultEntry(BaseModel):
    fault_id: str
    fault_type: str             # "missing_clause" | "risky_clause"
    section: str
    clause_id: str
    risk_level: str             # "low" | "medium" | "critical"
    description: str
    standard_language: Optional[str] = None   # for redline scoring
    is_trap: bool = False       # True = looks risky but is standard (false positive bait)
