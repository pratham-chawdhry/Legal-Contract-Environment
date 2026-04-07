"""
environment.py — Core OpenEnv-compliant Legal Contract Review environment.
"""
from __future__ import annotations
import copy
from typing import Any, Dict, List, Optional

from src.models import (
    ContractAction,
    ContractObservation,
    AgentFlag,
    SectionStatus,
    StepResult,
    FaultEntry,
)
from src.contracts import TASK_CONFIGS
from src.grader import grade_episode


MAX_STEPS_DEFAULT = 30

VALID_ACTIONS = {
    "read_section",
    "flag_clause",
    "mark_missing",
    "suggest_redline",
    "approve_section",
    "summarize",
}


class LegalContractEnv:
    """
    OpenEnv-compliant environment: Legal Contract Review.

    API:
        reset()  → ContractObservation
        step(action: ContractAction) → StepResult
        state()  → Dict
    """

    def __init__(self, task_id: str = "easy", max_steps: int = MAX_STEPS_DEFAULT):
        assert task_id in TASK_CONFIGS, f"Unknown task_id: {task_id}"
        self.task_id   = task_id
        self.max_steps = max_steps
        self._cfg      = TASK_CONFIGS[task_id]
        self._reset_internal()

    # ---------------------------------------------------------------- #
    # OpenEnv interface
    # ---------------------------------------------------------------- #

    def reset(self) -> ContractObservation:
        self._reset_internal()
        return self._build_observation("Environment reset. Review the contract.")

    def step(self, action: ContractAction) -> StepResult:
        if self._done:
            obs = self._build_observation("Episode already complete.")
            return StepResult(observation=obs, reward=0.0, done=True)

        self._step_count += 1
        reward, result_msg = self._dispatch(action)
        self._actions_taken.append(
            f"[{self._step_count}] {action.action_type}({action.params})"
        )

        # Check read-before-flag discipline
        if action.action_type in ("flag_clause", "mark_missing"):
            section = action.params.get("section", "")
            if section not in self._sections_read:
                reward -= 0.2
                result_msg += " ⚠️ Penalty: flagged without reading section first."

        # Time limit
        if self._step_count >= self.max_steps and not self._done:
            self._done = True
            result_msg += " Episode ended: max steps reached."

        obs = self._build_observation(result_msg)
        return StepResult(
            observation=obs,
            reward=round(reward, 4),
            done=self._done,
            info={"step": self._step_count},
        )

    def state(self) -> Dict[str, Any]:
        return {
            "task_id":        self.task_id,
            "step":           self._step_count,
            "done":           self._done,
            "pipeline_passed": self._passed,
            "flags":          [f.model_dump() for f in self._flags],
            "sections_read":  list(self._sections_read),
            "actions_taken":  self._actions_taken,
        }

    # ---------------------------------------------------------------- #
    # Internal helpers
    # ---------------------------------------------------------------- #

    def _reset_internal(self):
        self._step_count:    int           = 0
        self._done:          bool          = False
        self._passed:        bool          = False
        self._flags:         List[AgentFlag] = []
        self._sections_read: set           = set()
        self._redlines:      Dict[str, str] = {}
        self._approved:      set           = set()
        self._actions_taken: List[str]     = []
        self._last_section_text: Optional[str] = None
        self._last_section_name: Optional[str] = None
        self._fault_manifest: List[FaultEntry] = copy.deepcopy(self._cfg["faults"])

    def _dispatch(self, action: ContractAction):
        at = action.action_type
        p  = action.params

        if at not in VALID_ACTIONS:
            return -0.1, f"Unknown action '{at}'. Valid: {sorted(VALID_ACTIONS)}"

        if at == "read_section":
            return self._act_read_section(p)
        elif at == "flag_clause":
            return self._act_flag_clause(p, flag_type="risky")
        elif at == "mark_missing":
            return self._act_flag_clause(p, flag_type="missing")
        elif at == "suggest_redline":
            return self._act_suggest_redline(p)
        elif at == "approve_section":
            return self._act_approve_section(p)
        elif at == "summarize":
            return self._act_summarize()
        return -0.1, "Unhandled action."

    def _act_read_section(self, p):
        section = p.get("section", "")
        sections = self._cfg["sections"]
        if section not in sections:
            available = list(sections.keys())
            return -0.05, f"Section '{section}' not found. Available: {available}"
        self._sections_read.add(section)
        self._last_section_name = section
        self._last_section_text = sections[section]
        return 0.05, f"Read section '{section}' ({len(sections[section])} chars)."

    def _act_flag_clause(self, p, flag_type: str):
        section   = p.get("section", "")
        clause_id = p.get("clause_id", "")
        risk_level = p.get("risk_level", "medium")
        reason    = p.get("reason", "")

        if not section or not clause_id:
            return -0.1, "flag_clause requires 'section' and 'clause_id'."

        # Duplicate check
        for f in self._flags:
            if f.section == section and f.clause_id == clause_id:
                return -0.05, f"Already flagged {section}/{clause_id}."

        flag = AgentFlag(
            section=section,
            clause_id=clause_id,
            flag_type=flag_type,
            risk_level=risk_level,
            reason=reason,
        )
        self._flags.append(flag)
        return 0.1, f"Flagged {section}/{clause_id} as {flag_type} ({risk_level})."

    def _act_suggest_redline(self, p):
        clause_id = p.get("clause_id", "")
        text      = p.get("replacement_text", "")
        if not clause_id or not text:
            return -0.1, "suggest_redline requires 'clause_id' and 'replacement_text'."
        self._redlines[clause_id] = text
        # Mark the relevant flag as having a redline
        for f in self._flags:
            if f.clause_id == clause_id:
                f.redline_suggested = True
        return 0.05, f"Redline suggestion recorded for '{clause_id}'."

    def _act_approve_section(self, p):
        section = p.get("section", "")
        if section not in self._cfg["sections"]:
            return -0.05, f"Section '{section}' not found."
        self._approved.add(section)
        return 0.02, f"Section '{section}' marked as approved."

    def _act_summarize(self):
        grader_result, reward = grade_episode(self._flags, self._fault_manifest)
        score = grader_result.score
        self._passed = score >= 0.6
        self._done   = True

        msg = (
            f"Summary complete. Score={score:.2f} | "
            f"TP={grader_result.true_positives} | "
            f"FP={grader_result.false_positives} | "
            f"Missed criticals={grader_result.missed_criticals} | "
            f"Passed={self._passed}"
        )
        return reward, msg

    def _build_observation(self, last_result: str) -> ContractObservation:
        sections = self._cfg["sections"]
        statuses = [
            SectionStatus(
                section_name=s,
                read=(s in self._sections_read),
                approved=(s in self._approved),
                flags_count=sum(1 for f in self._flags if f.section == s),
            )
            for s in sections
        ]
        real_faults = [f for f in self._fault_manifest if not f.is_trap]
        matched = sum(
            1 for f in real_faults
            if any(
                af.section == f.section and (
                    af.clause_id == f.clause_id or
                    (af.flag_type == "risky"   and f.fault_type == "risky_clause") or
                    (af.flag_type == "missing" and f.fault_type == "missing_clause")
                )
                for af in self._flags
            )
        )

        return ContractObservation(
            task_id=self.task_id,
            difficulty=self._cfg["difficulty"],
            description=self._cfg["description"],
            max_steps=self.max_steps,
            contract_title=self._cfg["title"],
            available_sections=list(sections.keys()),
            section_statuses=statuses,
            current_section_text=self._last_section_text,
            current_section_name=self._last_section_name,
            flags=list(self._flags),
            actions_taken=self._actions_taken[-8:],
            last_action_result=last_result,
            step=self._step_count,
            done=self._done,
            pipeline_passed=self._passed,
            total_faults_in_contract=self._cfg["total_faults"],
            faults_found_so_far=matched,
        )