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

## Unattended daily submits (laptop off)

Primary path is **GitHub Actions** (same as Kaggriculture / Adaptive-Farm-Agent), not Cursor Cloud Automations.

Full write-up: [`agent/how-github-submits-work.md`](agent/how-github-submits-work.md).

### One-time setup

1. Repo on GitHub with Actions enabled.
2. [Settings → Secrets → Actions](https://github.com/ilakkmanoharan/casmi26-structure-prediction/settings/secrets/actions): add `KAGGLE_USERNAME`, `KAGGLE_KEY`, and preferably `OPENAI_API_KEY`.
3. **Actions → casmi-loop → Run workflow** once to verify.
4. Hourly cron runs `scripts/casmi_loop/orchestrate.py`; after 5 Chicago competition-day submits, later hours no-op.

```bash
# Manual / local one slot
PYTHONPATH=. python3 scripts/casmi_loop/orchestrate.py --slot 1
PYTHONPATH=. python3 scripts/casmi_loop/orchestrate.py --skip-submit   # docs+code only
```

### Optional

- **Grok Bot research (agent1 steps 1–3)** — skill [`.cursor/skills/casmi26-grok-research/SKILL.md`](.cursor/skills/casmi26-grok-research/SKILL.md) writes `Research/`, `Analysis/`, `Hypothesis analysis/` (and optional `Specs/`), commits, then dispatches `casmi-loop` for implement+submit.
- **Grok Bot watchdog** — skill [`.cursor/skills/casmi26-grok-watchdog/SKILL.md`](.cursor/skills/casmi26-grok-watchdog/SKILL.md) re-triggers Actions on failure / missed slots.
- Cursor Automations + [`agent/CLOUD_CYCLE_PROMPT.md`](agent/CLOUD_CYCLE_PROMPT.md) if you want an alternate agent runner.
- Local scaffolding: `python agent/run_daily_loop.py` / `python agent/run_cycle.py`

State schema: [`agent/state.schema.md`](agent/state.schema.md). Artifact folders: `Research/`, `Analysis/`, `Hypothesis analysis/`, `Specs/`.