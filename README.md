# Legal Contract Review — OpenEnv

An RL environment where an agent reviews legal contracts, identifies risks, missing clauses, and proposes redlines.

---

## Motivation

Legal teams review contracts daily — NDAs, SaaS agreements, M&A term sheets. Missing a liability cap or a buried auto-renewal clause can cost organisations millions. This environment simulates that workflow: the agent acts as a junior associate, reading sections, flagging risky clauses, detecting absent protections, suggesting replacement language, and producing a final signed-off review.

The environment is designed to benchmark agentic LLMs on tasks that require **sequential reasoning under a step budget**, **precision over recall** (false positives are penalised), and **discrimination between genuinely risky clauses and market-standard ones**.

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
| `MODEL_NAME` | No | `llama-3.3-70b-versatile` | Model to use |
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

### REST API (optional)

```bash
python -m uvicorn src.server:app --host 0.0.0.0 --port 7860
curl http://localhost:7860/health
```

---

## Environment Description

The environment follows the OpenEnv interface:

```python
env = LegalContractEnv(task_id="easy")   # "easy" | "medium" | "hard"
obs = env.reset()                         # → ContractObservation
result = env.step(action)                 # → StepResult
state = env.state()                       # → Dict
```

### Episode flow

1. `reset()` returns the initial observation: contract title, available sections, step counter, empty flag list.
2. The agent calls `step(action)` repeatedly until `done=True`.
3. `done` is set when the agent calls `summarize` or the step budget is exhausted.
4. `summarize` triggers the grader, which computes a score and sets `pipeline_passed`.

---

## Observation Space

Each step returns a `ContractObservation` with the following fields:

| Field | Type | Description |
|---|---|---|
| `task_id` | `str` | Task identifier: `"easy"`, `"medium"`, `"hard"` |
| `difficulty` | `str` | Human-readable difficulty label |
| `description` | `str` | Task description shown to the agent |
| `max_steps` | `int` | Maximum steps allowed this episode |
| `contract_title` | `str` | Title of the contract under review |
| `available_sections` | `List[str]` | All section names in this contract |
| `section_statuses` | `List[SectionStatus]` | Per-section read/approved/flag state |
| `current_section_text` | `Optional[str]` | Full text of the last read section |
| `current_section_name` | `Optional[str]` | Name of the last read section |
| `flags` | `List[AgentFlag]` | All flags raised so far (risky + missing) |
| `actions_taken` | `List[str]` | Recent action history (last 8) |
| `last_action_result` | `str` | Human-readable result of the last action |
| `step` | `int` | Current step number |
| `done` | `bool` | Whether the episode has ended |
| `pipeline_passed` | `bool` | Whether the episode score ≥ 0.6 |
| `total_faults_in_contract` | `int` | Ground-truth fault count (excluding traps) |
| `faults_found_so_far` | `int` | How many real faults the agent has matched |

### SectionStatus fields

| Field | Type | Description |
|---|---|---|
| `section_name` | `str` | Section identifier |
| `read` | `bool` | Whether the agent has read this section |
| `approved` | `bool` | Whether the agent has approved this section |
| `flags_count` | `int` | Number of flags raised in this section |

### AgentFlag fields

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

The agent submits actions as JSON objects. All actions are dispatched via `env.step(ContractAction(...))`.

### `read_section`

Read the full text of a contract section. Required before flagging anything in that section.

```json
{"action_type": "read_section", "params": {"section": "<section_name>"}}
```

**Reward:** `+0.05` per read. Penalty of `−0.20` if a flag or missing-clause action is taken on a section that has not been read.

---

### `flag_clause`

Mark a clause as risky or non-standard.

```json
{
  "action_type": "flag_clause",
  "params": {
    "section": "<section_name>",
    "clause_id": "<descriptive_id>",
    "risk_level": "low|medium|critical",
    "reason": "<explanation>"
  }
}
```

**Reward:** `+0.10` per flag raised. Additional grader rewards on `summarize` (see Grading).

---

### `mark_missing`

Flag a clause that is entirely absent from the contract but required by standard practice.

```json
{
  "action_type": "mark_missing",
  "params": {
    "section": "<section_where_clause_should_appear>",
    "clause_id": "<descriptive_id>",
    "risk_level": "low|medium|critical",
    "reason": "<what is absent and why it matters>"
  }
}
```

**Reward:** `+0.10` per flag raised. Additional grader rewards on `summarize`.

---

### `suggest_redline`

Propose replacement or insertion language for a previously flagged clause.

```json
{
  "action_type": "suggest_redline",
  "params": {
    "clause_id": "<same_id_used_in_flag>",
    "replacement_text": "<standard language>"
  }
}
```

**Reward:** `+0.05` for recording the redline. Additional `+0.30` from the grader if the replacement text matches the standard language for that fault.

---

### `approve_section`

Mark a section as reviewed and acceptable, with no issues found.

```json
{"action_type": "approve_section", "params": {"section": "<section_name>"}}
```

**Reward:** `+0.02`.

---

### `summarize`

End the episode and trigger grading. Must be called explicitly — hitting the step limit without calling `summarize` produces a graded result but typically a lower score.

```json
{"action_type": "summarize", "params": {}}
```

**Reward:** Determined by the grader (see Grading).

---

## Task Descriptions

### easy — Mutual NDA (Acme Corp / Beta Ventures)

A one-page mutual non-disclosure agreement. The agent reviews 7 sections for missing protective clauses and non-standard terms before the agreement is signed.

| Fault | Type | Section | Risk | Description |
|---|---|---|---|---|
| F1 | Missing clause | `obligations` | Critical | No liability cap — unlimited financial exposure for any breach |
| F2 | Risky clause | `obligations` | Critical | Uncapped, one-sided indemnification with no carve-outs or notice requirement |

**Sections:** `parties`, `purpose`, `definition_confidential`, `obligations`, `term`, `governing_law`, `general`

**Expected difficulty:** An agent that reads all sections and has basic NDA knowledge should catch both faults within 15 steps.

**Baseline score (glm-5:cloud):** 1.00 | 2.82 reward | 15 steps

---

### medium — SaaS Subscription Agreement (Vendor / Customer)

An 8-page software-as-a-service agreement. The agent reviews 9 sections for predatory clauses, missing SLA commitments, and non-standard IP terms.

| Fault | Type | Section | Risk | Description |
|---|---|---|---|---|
| F1 | Risky clause | `definitions` | Medium | Auto-renewal with 15% price escalation buried inside the `Subscription Term` definition, not in the termination section |
| F2 | Risky clause | `intellectual_property` | Critical | Irrevocable, perpetual, sublicensable data license that survives termination — Customer permanently loses control of their data |
| F3 | Missing clause | `data_privacy` | Medium | No SLA or uptime commitment anywhere in the agreement |

**Sections:** `definitions`, `license_grant`, `fees_payment`, `data_privacy`, `intellectual_property`, `warranties`, `limitation_liability`, `term_termination`, `general`

**Expected difficulty:** Requires pattern-matching on predatory drafting (clause buried in wrong section) and recognising a missing SLA, which has no text to read and must be inferred from absence.

**Baseline score (glm-5:cloud):** 1.00 | 3.60 reward | 25 steps

---

### hard — M&A Term Sheet (Meridian Capital / Nova Systems)

A 20-page M&A term sheet for a $42M asset acquisition. The agent reviews 10 sections including schedules. Some clauses look risky but are market-standard — **accurate discrimination is required**. Flagging market-standard clauses is penalised.

| Fault | Type | Section | Risk | Description |
|---|---|---|---|---|
| F1 | Risky clause | `schedule_a_open_source` | Critical | 34% of Target's codebase is GPLv3-licensed; distribution by Acquirer triggers copyleft obligations requiring source code disclosure. Remediation: $180K–$400K or 8–14 months engineering |
| F2 | Risky clause | `schedule_b_earnout_definition` | Medium | Acquirer has sole discretion over ARR calculation; CFO-approval gate on channel partner revenue allows suppression of the $5M earnout |
| F3 | Missing clause | `conditions_closing` | Medium | No R&W insurance mentioned — market standard for a $42M deal, would allow escrow reduction |
| F4 (trap) | — | `indemnification` | — | 1% tipping basket is market-standard — flagging this is a false positive |
| F5 (trap) | — | `representations_warranties` | — | 18-month rep survival is within market range — flagging this is a false positive |

**Sections:** `transaction_summary`, `purchase_price_adjustment`, `representations_warranties`, `indemnification`, `intellectual_property`, `employee_matters`, `conditions_closing`, `exclusivity_no_shop`, `schedule_a_open_source`, `schedule_b_earnout_definition`

**Expected difficulty:** Hard. The agent must read schedules (not just main sections), recognise GPLv3 copyleft risk without being told, understand earnout manipulation structures, and correctly ignore two trap clauses that look suspicious but are standard.

**Baseline score (glm-5:cloud):** 1.00 | 4.19 reward | 24 steps

---

## Grading

Grading runs when the agent calls `summarize`. The grader compares the agent's flags against a ground-truth fault manifest.

### Matching rule

A flag is a **true positive** if it matches an unmatched real fault in the same section with the same broad fault type:

- `flag_type="risky"` matches `fault_type="risky_clause"`
- `flag_type="missing"` matches `fault_type="missing_clause"`

The agent does not need to supply the exact manifest `clause_id` — section + type is sufficient. Each agent flag may match at most one fault.

### Score formula

```
recall    = true_positives / total_real_faults
precision = true_positives / (true_positives + false_positives)
f_score   = 2 * recall * precision / (recall + precision)
score     = max(0, f_score − 0.3 * missed_criticals / total_real_faults)
```

**Pipeline passes when `score ≥ 0.6`.**

### Reward table

| Event | Reward |
|---|---|
| `read_section` | +0.05 |
| `approve_section` | +0.02 |
| `flag_clause` or `mark_missing` | +0.10 |
| `suggest_redline` | +0.05 |
| Flag without reading section first | −0.20 |
| True positive — critical fault | +0.80 |
| True positive — medium fault | +0.60 |
| True positive — low fault | +0.40 |
| Correct `risk_level` on true positive | +0.10 |
| Redline matches standard language | +0.30 |
| False positive | −0.40 |
| False positive on trap clause | −0.40 − 0.20 extra |
| Missed critical fault | −1.00 |

---

## Baseline Scores

All baselines use `glm-5:cloud` via Ollama, `MAX_STEPS=30`, `TEMPERATURE=0.1`.

| Task | Score | Reward | Steps | Faults caught | Passed |
|---|---|---|---|---|---|
| easy | 1.00 | +2.82 | 15 | 2/2 | Yes |
| medium | 1.00 | +3.60 | 25 | 3/3 | Yes |
| hard | 1.00 | +4.19 | 24 | 3/3 | Yes |
| **average** | **1.00** | **+3.54** | **21** | — | **3/3** |

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

## Extension Points

- **Add tasks:** Define new sections and `FaultEntry` manifests in `contracts.py`, register in `TASK_CONFIGS`.
- **Swap models:** Set `MODEL_NAME` env var or replace the `ollama.chat(...)` call in `inference.py` with any OpenAI-compatible client.
- **Harder traps:** Add more `is_trap=True` entries to a fault manifest to raise the false-positive penalty surface.
- **RL training:** The `step()` API is compatible with standard RL loops. `StepResult.reward` is the per-step signal; `StepResult.done` is the terminal flag.
