---
title: Legal Contract Review — OpenEnv
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
license: mit
---

# Legal Contract Review — OpenEnv

An RL environment where an agent reviews legal contracts, identifies risks, detects missing clauses, and proposes fixes.

---

## Motivation

Legal teams review contracts daily — NDAs, SaaS agreements, M&A term sheets. Missing a liability cap or a buried auto-renewal clause can cost organisations millions. This environment simulates that workflow: the agent acts as a junior associate, reading sections sequentially, flagging risky or non-standard clauses, detecting absent protections, suggesting replacement language, and producing a final signed-off review.

The environment benchmarks agentic LLMs on tasks that require **sequential reasoning under a step budget**, **precision** (false positives are penalised), and **discrimination** between genuinely risky clauses and market-standard ones.

---

## Project Structure

```
legal_contract_env/
├── inference.py          Agent loop, prompt builder, action parser
├── openenv.yaml          OpenEnv manifest
├── requirements.txt
├── Dockerfile
└── src/
    ├── __init__.py
    ├── contracts.py      Synthetic contracts + ground-truth fault manifests
    ├── environment.py    OpenEnv-compliant env (reset / step / state)
    ├── grader.py         Deterministic grader (F1-weighted, recall-focused)
    ├── models.py         Pydantic models (ContractAction, ContractObservation, …)
    └── server.py         FastAPI REST wrapper
```

---

## Setup

```bash
git clone <repo>
cd legal_contract_env
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | Yes | — | API key for Groq inference |
| `MODEL_NAME` | No | `llama-3.3-70b-versatile` | Model override |
| `MAX_STEPS` | No | `30` | Max steps per episode |
| `TEMPERATURE` | No | `0.1` | Sampling temperature |
| `MAX_TOKENS` | No | `500` | Max tokens per LLM call |

```bash
export GROQ_API_KEY="your_key_here"
export MODEL_NAME="llama-3.3-70b-versatile"
```

---

## Usage

```bash
# Run all three tasks
python inference.py

# Run a specific task
python inference.py --task easy
python inference.py --task medium
python inference.py --task hard

# Override step budget
python inference.py --task hard --steps 35

# Suppress per-step output
python inference.py --quiet
```

### REST API

```bash
python -m uvicorn server.app:app --host 0.0.0.0 --port 7860

# Health check
curl http://localhost:7860/health

# Start a session
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy", "max_steps": 30}'

# Take a step
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<id>", "action": {"action_type": "read_section", "params": {"section": "obligations"}}}'

# List available tasks
curl http://localhost:7860/tasks
```

---

## Environment Description

The environment follows the OpenEnv interface:

```python
from src.environment import LegalContractEnv
from src.models import ContractAction

env = LegalContractEnv(task_id="easy")  # "easy" | "medium" | "hard"
obs = env.reset()                        # → ContractObservation
result = env.step(action)                # → StepResult
state = env.state()                      # → Dict
```

### Episode flow

1. `reset()` returns the initial `ContractObservation`: contract title, available sections, empty flag list.
2. The agent calls `step(ContractAction(...))` repeatedly.
3. `done` becomes `True` when the agent calls `summarize` or the step budget is exhausted.
4. `summarize` triggers the grader, which computes a score ∈ [0, 1] and sets `pipeline_passed = score ≥ 0.6`.

---

## Observation Space

Each `step()` returns a `StepResult` containing a `ContractObservation`:

| Field | Type | Description |
|---|---|---|
| `task_id` | `str` | Task identifier: `"easy"`, `"medium"`, `"hard"` |
| `difficulty` | `str` | Human-readable difficulty label |
| `description` | `str` | Task description shown to the agent |
| `max_steps` | `int` | Maximum steps allowed this episode |
| `contract_title` | `str` | Title of the contract under review |
| `available_sections` | `List[str]` | All section names in this contract |
| `section_statuses` | `List[SectionStatus]` | Per-section read / approved / flag state |
| `current_section_text` | `Optional[str]` | Full text of the last read section |
| `current_section_name` | `Optional[str]` | Name of the last read section |
| `flags` | `List[AgentFlag]` | All flags raised so far (risky + missing) |
| `actions_taken` | `List[str]` | Recent action history (last 8 entries) |
| `last_action_result` | `str` | Human-readable result of the last action |
| `step` | `int` | Current step number |
| `done` | `bool` | Whether the episode has ended |
| `pipeline_passed` | `bool` | `True` when `summarize` is called with score ≥ 0.6 |
| `total_faults_in_contract` | `int` | Ground-truth fault count (traps excluded) |
| `faults_found_so_far` | `int` | How many real faults the agent has matched so far |

### `SectionStatus` sub-model

| Field | Type | Description |
|---|---|---|
| `section_name` | `str` | Section identifier |
| `read` | `bool` | Whether the agent has read this section |
| `approved` | `bool` | Whether the agent has approved this section |
| `flags_count` | `int` | Number of flags raised in this section |

### `AgentFlag` sub-model

| Field | Type | Description |
|---|---|---|
| `section` | `str` | Section the flag belongs to |
| `clause_id` | `str` | Descriptive identifier chosen by the agent |
| `flag_type` | `str` | `"risky"` or `"missing"` |
| `risk_level` | `str` | `"low"`, `"medium"`, or `"critical"` |
| `reason` | `str` | Agent's explanation |
| `redline_suggested` | `bool` | Whether a redline has been submitted for this flag |

---

## Action Space

All actions are submitted as `ContractAction(action_type=..., params={...})`.

### `read_section`

Read the full text of a contract section. Must be called before flagging anything in that section.

```json
{"action_type": "read_section", "params": {"section": "<section_name>"}}
```

Reward: `+0.05`. Penalty of `−0.20` is applied on any subsequent flag action if the section was not read first.

---

### `flag_clause`

Mark a clause as risky or non-standard.

```json
{
  "action_type": "flag_clause",
  "params": {
    "section": "<section_name>",
    "clause_id": "<descriptive_id e.g. 'unlimited_indemnity'>",
    "risk_level": "low|medium|critical",
    "reason": "<concrete explanation>"
  }
}
```

Reward: `+0.10` at call time. Additional grader rewards apply at `summarize`.

---

### `mark_missing`

Flag a clause that is entirely absent from the contract but required by standard practice.

```json
{
  "action_type": "mark_missing",
  "params": {
    "section": "<section where clause should appear>",
    "clause_id": "<descriptive_id e.g. 'liability_cap'>",
    "risk_level": "low|medium|critical",
    "reason": "<what is absent and why it matters>"
  }
}
```

Reward: `+0.10` at call time. Additional grader rewards apply at `summarize`.

---

### `suggest_redline`

Propose replacement or insertion language for a previously flagged clause.

```json
{
  "action_type": "suggest_redline",
  "params": {
    "clause_id": "<same id used in flag_clause or mark_missing>",
    "replacement_text": "<standard language>"
  }
}
```

Reward: `+0.05` for recording. Additional `+0.30` from the grader if the replacement text matches the fault's standard language.

---

### `approve_section`

Mark a section as reviewed and acceptable, with no issues found.

```json
{"action_type": "approve_section", "params": {"section": "<section_name>"}}
```

Reward: `+0.02`.

---

### `summarize`

End the episode and trigger grading. Should be called explicitly after all sections are reviewed.

```json
{"action_type": "summarize", "params": {}}
```

Reward: determined by the grader (see Grading below).

---

## Grading

Grading runs when the agent calls `summarize`. The grader (`src/grader.py`) compares the agent's flags against a hidden ground-truth fault manifest.

### Matching rule

A flag is a **true positive** if it matches an unmatched real fault in the **same section** with the **same broad fault type**:

- `flag_type="risky"` matches `fault_type="risky_clause"`
- `flag_type="missing"` matches `fault_type="missing_clause"`

The agent does not need to supply the exact manifest `clause_id` — section + type match is sufficient. Each agent flag can match at most one fault.

### Score formula

```
recall    = true_positives / total_real_faults
precision = true_positives / (true_positives + false_positives)
f_score   = 2 × recall × precision / (recall + precision)
score     = max(0, f_score − 0.3 × missed_criticals / total_real_faults)
```

**Pipeline passes when `score ≥ 0.6`.**

### Reward table

| Event | Reward |
|---|---|
| `read_section` | +0.05 |
| `approve_section` | +0.02 |
| `flag_clause` or `mark_missing` (at call time) | +0.10 |
| `suggest_redline` (at call time) | +0.05 |
| Flag without reading section first | −0.20 |
| True positive — critical fault | +0.80 |
| True positive — medium fault | +0.60 |
| True positive — low fault | +0.40 |
| Correct `risk_level` on true positive | +0.10 |
| Redline matches standard language | +0.30 |
| Missed critical fault | −1.00 |

---

## Task Descriptions

### easy — Mutual NDA (Acme Corp / Beta Ventures)

A one-page mutual non-disclosure agreement. The agent reviews 7 sections for missing protective clauses and non-standard terms before signing.

**Sections:** `parties`, `purpose`, `definition_confidential`, `obligations`, `term`, `governing_law`, `general`

| Fault | Type | Section | Risk | Description |
|---|---|---|---|---|
| F1 | Missing clause | `obligations` | Critical | No liability cap — unlimited financial exposure for any breach |
| F2 | Risky clause | `obligations` | Critical | Uncapped, one-sided indemnification with no carve-outs or notice requirement |

**Expected difficulty:** Straightforward. Both faults are in the same section and visible on a single read. An agent that reads all sections and has basic NDA knowledge should catch both within 15 steps.

---

### medium — SaaS Subscription Agreement (Vendor / Customer)

An 8-page software-as-a-service agreement. The agent reviews 9 sections for predatory clauses, missing SLA commitments, and non-standard IP terms.

**Sections:** `definitions`, `license_grant`, `fees_payment`, `data_privacy`, `intellectual_property`, `warranties`, `limitation_liability`, `term_termination`, `general`

| Fault | Type | Section | Risk | Description |
|---|---|---|---|---|
| F1 | Risky clause | `definitions` | Medium | Auto-renewal with 15% price escalation buried inside the `Subscription Term` definition — not in the termination section where a customer would look |
| F2 | Risky clause | `intellectual_property` | Critical | Irrevocable, perpetual, sublicensable data license surviving termination — Customer permanently loses control of their data |
| F3 | Missing clause | `data_privacy` | Medium | No SLA or uptime commitment anywhere in the agreement |

**Expected difficulty:** Moderate. Requires recognising a predatory drafting pattern (clause buried in wrong section) and detecting a missing SLA that has no text to read — it must be inferred from absence.

---

### hard — M&A Term Sheet (Meridian Capital / Nova Systems)

A 20-page M&A term sheet for a $42M asset acquisition. The agent reviews 10 sections including schedules. Two clauses are **trap clauses** — they resemble risks but are market-standard. Flagging them is penalised.

**Sections:** `transaction_summary`, `purchase_price_adjustment`, `representations_warranties`, `indemnification`, `intellectual_property`, `employee_matters`, `conditions_closing`, `exclusivity_no_shop`, `schedule_a_open_source`, `schedule_b_earnout_definition`

| Fault | Type | Section | Risk | Description |
|---|---|---|---|---|
| F1 | Risky clause | `schedule_a_open_source` | Critical | 34% of codebase is GPLv3-licensed with no commercial license; distribution by Acquirer triggers copyleft obligations. Remediation: $180K–$400K or 8–14 months of engineering |
| F2 | Risky clause | `schedule_b_earnout_definition` | Medium | Acquirer has sole discretion over ARR calculation; CFO-approval gate on channel partner revenue allows suppression of the $5M earnout |
| F3 | Missing clause | `conditions_closing` | Medium | No R&W insurance — market standard for a $42M deal, would allow escrow reduction from 10% to 5% |
| F4 *(trap)* | — | `indemnification` | — | 1% tipping basket is market-standard — flagging it is a false positive |
| F5 *(trap)* | — | `representations_warranties` | — | 18-month rep survival is within market range — flagging it is a false positive |

**Expected difficulty:** Hard. The agent must read schedules (not just main sections), understand GPLv3 copyleft mechanics, recognise earnout manipulation structure, and correctly ignore two trap clauses that superficially resemble risks.

---

## Baseline Scores

Model: `glm-5:cloud` via Ollama. Configuration: `MAX_STEPS=30`, `TEMPERATURE=0.1`.

| Task | Score | Reward | Steps | Faults caught | Passed |
|---|---|---|---|---|---|
| easy | 1.00 | +2.82 | 15 | 2 / 2 | Yes |
| medium | 1.00 | +3.60 | 25 | 3 / 3 | Yes |
| hard | 1.00 | +4.19 | 24 | 3 / 3 | Yes |
| **average** | **1.00** | **+3.54** | **21** | — | **3 / 3** |

---

## Extension Points

- **Add tasks:** Define new section dicts and `FaultEntry` lists in `contracts.py`, register them in `TASK_CONFIGS`.
- **Swap models:** Set `MODEL_NAME` or replace the `ollama.chat(...)` call in `inference.py` with any OpenAI-compatible client.
- **Add traps:** Include more `FaultEntry(is_trap=True, ...)` entries to raise the false-positive difficulty surface.
- **RL training:** The `step()` API is compatible with standard RL loops — `StepResult.reward` is the per-step signal, `StepResult.done` is the terminal flag.
