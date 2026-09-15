# Enveda CASMI 2026 — Structure prediction

Retrieval-first baseline with an explicit adduct / mass symbolic world model for
[Enveda CASMI 2026 — Molecule ID From Mass Spectra](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra).

## Setup

```bash
pip install -r requirements.txt
export PATH="$HOME/Library/Python/3.9/bin:$PATH"   # if needed for kaggle CLI
kaggle competitions download -c enveda-CASMI26-molecule-id-mass-spectra -p data
# rename DownloadDataFile → train.parquet / test.parquet if the CLI uses that name
```

## Run

```bash
PYTHONPATH=. python scripts/run_pipeline.py
```

Outputs (gitignored):

- `outputs/submission.csv`
- `outputs/candidate_evidence.parquet`
- `outputs/run_summary.json`
- `artifacts/spectrum_index.npz`

## Tests

```bash
python -m pytest tests/ -q
```

## Submit (notebook-only competition)

Direct CSV upload is rejected. Push and score via the Kaggle notebook:

```bash
# offline RDKit wheels dataset:
#   ilakkmanoharan/rdkit-cp312-wheels-casmi26

kaggle kernels push -p kaggle_kernel
# wait until COMPLETE, then:
python - <<'PY'
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi(); api.authenticate()
print(api.competition_submit_code(
    file_name='submission.csv',
    message='retrieval+symbolic',
    competition='enveda-CASMI26-molecule-id-mass-spectra',
    kernel='ilakkmanoharan/casmi26-retrieval-symbolic-v01',
))
PY
```

Notebook: https://www.kaggle.com/code/ilakkmanoharan/casmi26-retrieval-symbolic-v01

## Cloud Automations (laptop off)

Primary daily loop runs on **Cursor Cloud Automations** so submissions continue when this machine is off.

### One-time UI setup

1. Connect GitHub to Cursor (Cloud Agents can clone this repo).
2. Open [cursor.com/automations](https://cursor.com/automations) → create automation.
3. **Trigger:** scheduled / cron for competition day slots after **01:00 America/Chicago** every ~90 minutes (five slots; see [`agent/CLOUD_CYCLE_PROMPT.md`](agent/CLOUD_CYCLE_PROMPT.md) for UTC examples).
4. **Repository:** select `ilakkmanoharan/casmi26-structure-prediction` (required — cron defaults to no repo).
5. **Prompt:** instruct the agent to follow [`agent/CLOUD_CYCLE_PROMPT.md`](agent/CLOUD_CYCLE_PROMPT.md) end-to-end (research → analysis → hypothesis → spec → implement → Kaggle code submit → update `agent/state.json` → commit/push).
6. **Secrets** (Cloud Agents / environment): `KAGGLE_USERNAME`, `KAGGLE_KEY`.

Repo Cloud env install: [`.cursor/environment.json`](.cursor/environment.json).

### Local fallback

```bash
PYTHONPATH=. python agent/run_daily_loop.py
PYTHONPATH=. python agent/run_cycle.py
```

State schema: [`agent/state.schema.md`](agent/state.schema.md). Artifact folders: `Research/`, `Analysis/`, `Hypothesis analysis/`, `Specs/`.
