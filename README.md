## Clara Automation Pipeline

Zero-cost, local-only automation pipeline for **"Clara Answers Intern Assignment"**.

The pipeline converts demo call and onboarding transcripts into structured **Account Memo JSON** and **Retell Agent Draft Spec JSON** configurations, with versioned outputs and changelogs.

**Author**: Shreya Kumari

---

### Architecture Diagram
<img width="2241" height="2002" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/ffb49a18-d67a-4451-8b62-359fc5c40750" />


### Repository Structure

clara-automation-pipeline/
  dataset/
  demo_calls/
    <account_id>/
      chat.txt
  onboarding_calls/
    <account_id>/
      chat.txt
  scripts/
    extract_account_data.py
    generate_agent_prompt.py
    apply_patch.py
    diff_generator.py
    run_all.py
  outputs/
    accounts/
      <account_id>/
        v1/
          memo.json
          agent.json
        v2/
          memo.json
          agent.json
          changelog.md
  workflows/
    n8n_workflow.json
  docker-compose.yml
  README.md

---

### What the Pipeline Produces

For each account (`<account_id>` inferred from the folder name under `demo_calls/`):

- **v1 (demo-derived)**:
  - `outputs/accounts/<account_id>/v1/memo.json`
  - `outputs/accounts/<account_id>/v1/agent.json`
- **v2 (onboarding-confirmed)** (only if onboarding data exists):
  - `outputs/accounts/<account_id>/v2/memo.json`
  - `outputs/accounts/<account_id>/v2/agent.json`
  - `outputs/accounts/<account_id>/v2/changelog.md` (diff between v1 and v2)

Versioning is **idempotent**: re-running regenerates the same paths (no duplicates), and preserves the v1/v2 separation.

Logging is also produced (overwritten each run to keep outputs idempotent):
- **Global log**: `outputs/pipeline.log`
- **Per-account log**: `outputs/accounts/<account_id>/pipeline.log`

A free “task tracker” mock is produced as a local file:
- **Task tracker**: `outputs/tasks.json` (one task per account per stage)

---

### Setup Instructions (Local, Zero-Cost)

This project uses **Python standard library only** (no paid APIs, no external SDKs).

```bash
cd clara-automation-pipeline
python -m venv .venv

# PowerShell
. .venv/Scripts/Activate.ps1

python --version
```

---

### Transcript Inputs

Create account folders and place transcripts:

```text
demo_calls/<account_id>/chat.txt
onboarding_calls/<account_id>/chat.txt         (optional)
onboarding_calls/<account_id>/form.json        (optional structured form)
```

**Rules**:
- The pipeline **never invents** missing values.
- Anything not explicitly stated goes into **`questions_or_unknowns`**.
- Onboarding transcript and form data **override** demo-derived values when present.
- Structured form overrides are recorded in `notes` as explicit conflict messages.

---

### How to Run (Batch)

From `clara-automation-pipeline/`:

```bash
python scripts/run_all.py
```

Optional flags:

```bash
python scripts/run_all.py --root . --demo-dir demo_calls --onboarding-dir onboarding_calls --outputs-dir outputs
```

---

### n8n (Optional, Local via Docker)

Start n8n:

```bash
docker-compose up -d
```

Then import `workflows/n8n_workflow.json` into the n8n UI (`http://localhost:5678`).
The included workflow exposes a webhook and runs:

```text
python scripts/run_all.py --root /data
```

---

### Output Schemas

#### Account Memo (`memo.json`)
Required keys (always present):
- `account_id`
- `company_name`
- `business_hours` (object with `days`, `start`, `end`, `timezone`, `raw`)
- `office_address`
- `services_supported` (list)
- `emergency_definition` (list of triggers)
- `emergency_routing_rules` (object with `raw`, `steps`)
- `non_emergency_routing_rules` (object with `raw`, `steps`)
- `call_transfer_rules` (object with `raw`, optional `timeout_seconds`, optional `retries`)
- `integration_constraints`
- `after_hours_flow_summary`
- `office_hours_flow_summary`
- `questions_or_unknowns`
- `notes`

#### Agent Spec (`agent.json`)
Required keys:
- `agent_name`
- `voice_style`
- `system_prompt`
- `key_variables`
- `tool_invocation_placeholders` (internal-only placeholders)
- `call_transfer_protocol`
- `fallback_protocol`
- `version`

---

### Retell Setup (Manual Import)

If Retell free tier does not allow programmatic agent creation, use the generated `agent.json` as the “draft spec”:

- Open Retell UI and create a new agent.
- Copy/paste:
  - `agent_name`
  - `voice_style` (choose a similar voice/tones in UI)
  - `system_prompt` (paste into the system prompt field)
- Keep `tool_invocation_placeholders` as internal engineering notes only (do **not** expose to callers).

This repository intentionally does **not** call Retell APIs to preserve the zero-cost constraint and reproducibility.

The `system_prompt` explicitly includes:
- Business hours call flow
- After-hours call flow
- Emergency handling
- Transfer failure handling
- Caller closing procedure

---

### Limitations

- **Heuristic extraction**: Parsing is rule-based (regex/keywords), so some transcripts won’t yield structured fields without clearer phrasing.
- **No audio transcription**: Assumes `chat.txt` already exists.
- **No external integrations**: Integration constraints are captured as text, not enforced via API calls.

---


