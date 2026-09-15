# Enveda CASMI 2026 — First Submission

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
PYTHONPATH=. python scripts/run_pipeline.py --preferred-libs-only
```

Outputs:

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
# offline RDKit wheels dataset (already created):
#   ilakkmanoharan/rdkit-cp312-wheels-casmi26

kaggle kernels push -p kaggle_kernel
# wait until COMPLETE, then:
python - <<'PY'
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi(); api.authenticate()
print(api.competition_submit_code(
    file_name='submission.csv',
    message='v0.1 retrieval+symbolic',
    competition='enveda-CASMI26-molecule-id-mass-spectra',
    kernel='ilakkmanoharan/casmi26-retrieval-symbolic-v01',
))
PY
```

Notebook: https://www.kaggle.com/code/ilakkmanoharan/casmi26-retrieval-symbolic-v01
