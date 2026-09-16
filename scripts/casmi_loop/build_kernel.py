"""Rebuild kaggle_kernel notebook by embedding current casmi26/*.py sources."""

from __future__ import annotations

import json
from pathlib import Path

from .config import KERNEL_DIR, PACKAGE_DIR, ROOT

RDKIT_BOOTSTRAP = """import sys, subprocess
from pathlib import Path

def _ensure_rdkit():
    try:
        import rdkit  # noqa: F401
        return
    except Exception:
        pass
    inp = Path('/kaggle/input')
    links = []
    if inp.exists():
        for whl in inp.rglob('*.whl'):
            parent = str(whl.parent)
            if parent not in links:
                links.append(parent)
        for d in inp.iterdir():
            if d.is_dir() and 'rdkit' in d.name.lower():
                p = str(d)
                if p not in links:
                    links.append(p)
    if not links:
        raise RuntimeError('rdkit missing and no local wheels under /kaggle/input')
    cmd = [sys.executable, '-m', 'pip', 'install', '--no-index', '--no-deps']
    for link in links:
        cmd.extend(['--find-links', link])
    cmd.append('rdkit')
    print('installing rdkit from local wheels', links)
    subprocess.check_call(cmd)

_ensure_rdkit()
"""

MODULE_ORDER = [
    "adducts",
    "chemistry",
    "spectrum",
    "config",
    "index",
    "retrieve",
    "submission",
    "metrics",
]


def _code_cell(source: str, cell_id: str) -> dict:
    text = source if source.endswith("\n") else source + "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def _embed_cell(sources: dict[str, str]) -> str:
    parts = [
        RDKIT_BOOTSTRAP.rstrip(),
        "import sys, os, time, json, random, types",
        "from pathlib import Path",
        "import numpy as np, pandas as pd, pyarrow, pyarrow.parquet as pq",
        "from rdkit import Chem, RDLogger",
        "RDLogger.DisableLog('rdApp.*')",
        "print('python', sys.version.split()[0])",
        "print('numpy', np.__version__, 'pandas', pd.__version__, 'pyarrow', pyarrow.__version__)",
        "print('rdkit', Chem.rdBase.rdkitVersion)",
        "SEED=42; random.seed(SEED); np.random.seed(SEED)",
        "",
        "DATA=None",
        "for p in [",
        "    Path('/kaggle/input/enveda-CASMI26-molecule-id-mass-spectra'),",
        "    Path('/kaggle/input/competitions/enveda-CASMI26-molecule-id-mass-spectra'),",
        "]:",
        "    if (p/'test.parquet').exists():",
        "        DATA=p; break",
        "if DATA is None:",
        "    hits=list(Path('/kaggle/input').rglob('test.parquet'))",
        "    assert hits, 'test.parquet not found under /kaggle/input'",
        "    DATA=hits[0].parent",
        "print('DATA', DATA)",
        "OUT=Path('/kaggle/working'); ART=OUT/'artifacts'; ART.mkdir(parents=True, exist_ok=True)",
        "PKG=OUT/'casmi26_pkg'; (PKG/'casmi26').mkdir(parents=True, exist_ok=True)",
        "sys.path.insert(0, str(PKG))",
        "",
        "SOURCES = {",
    ]
    for name, src in sources.items():
        parts.append("    %r: %r," % (name, src))
    parts.extend(
        [
            "}",
            "(PKG/'casmi26'/'__init__.py').write_text('__version__=\"0.1.0\"\\n')",
            "for name, src in SOURCES.items():",
            "    (PKG/'casmi26'/f'{name}.py').write_text(src)",
            "print('embedded casmi26 modules:', sorted(SOURCES))",
            "",
        ]
    )
    return "\n".join(parts)


INFER_CELL = """from casmi26.config import RunConfig, PREFERRED_LIBS
from casmi26.index import build_index_from_train
from casmi26.retrieve import aggregate_molecule_candidates
from casmi26.submission import build_submission_frame, validate_submission, write_submission
from tqdm.auto import tqdm

cfg = RunConfig()
print(json.dumps(cfg.to_dict(), indent=2))
t0=time.time()
index = build_index_from_train(
    DATA/'train.parquet', cfg, cache_path=ART/'spectrum_index.npz', libraries=None,
)
print(f'index size={len(index.neutral_mass)} build_elapsed={time.time()-t0:.1f}s')

test_df = pq.read_table(DATA/'test.parquet').to_pandas()
sample = pd.read_csv(DATA/'sample_submission.csv')
print('test rows', len(test_df), 'molecules', test_df.molecule_id.nunique())

predictions={}; evidence_rows=[]; stats={'fallback_molecules':0,'placeholder_molecules':0,'n_candidates_total':0}
t1=time.time()
for molecule_id, g in tqdm(list(test_df.groupby('molecule_id', sort=False)), desc='infer'):
    cands, diag = aggregate_molecule_candidates(molecule_id, g, index, cfg)
    predictions[molecule_id]=[c.smiles for c in cands]
    stats['fallback_molecules'] += int(bool(diag.get('fallback_used')))
    stats['placeholder_molecules'] += int(bool(diag.get('placeholder_used')))
    stats['n_candidates_total'] += len(cands)
    for rank,c in enumerate(cands,1):
        row=c.to_dict(); row.update({'molecule_id':molecule_id,'rank':rank,'neutral_mass':diag.get('neutral_mass')})
        evidence_rows.append(row)
stats['elapsed_sec']=time.time()-t1
stats['n_molecules']=len(predictions)
print('inference', stats)

sub = build_submission_frame(predictions, sample)
errors = validate_submission(sub, sample, test_molecule_ids=test_df.molecule_id.unique())
assert not errors, errors
write_submission(sub, OUT/'submission.csv')
pd.DataFrame(evidence_rows).to_parquet(OUT/'candidate_evidence.parquet', index=False)
cand_counts = sub['smiles'].apply(lambda s: len(str(s).split(';')))
summary={
  'n_rows': len(sub),
  'candidate_count_mean': float(cand_counts.mean()),
  'candidate_count_min': int(cand_counts.min()),
  'candidate_count_max': int(cand_counts.max()),
  'stats': stats,
  'index_size': int(len(index.neutral_mass)),
  'total_elapsed_sec': time.time()-t0,
}
print('=== RUN SUMMARY ===')
print(json.dumps(summary, indent=2))
(OUT/'run_summary.json').write_text(json.dumps(summary, indent=2))
print('Wrote', OUT/'submission.csv')
display(sub.head())
"""


def load_package_sources() -> dict[str, str]:
    sources: dict[str, str] = {}
    for name in MODULE_ORDER:
        path = PACKAGE_DIR / ("%s.py" % name)
        if not path.is_file():
            raise SystemExit("missing package module: %s" % path)
        sources[name] = path.read_text(encoding="utf-8")
    return sources


def rebuild_kernel(*, title: str = "CASMI loop submission") -> Path:
    """Write kaggle_kernel/ notebook + metadata from current casmi26 package."""
    KERNEL_DIR.mkdir(parents=True, exist_ok=True)
    sources = load_package_sources()
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "cells": [
            {
                "cell_type": "markdown",
                "id": "casmi-md",
                "metadata": {},
                "source": [
                    "# Enveda CASMI 2026 — Retrieval + Symbolic\n",
                    "\n",
                    "%s\n" % title,
                    "\n",
                    "Internet **off**. Output: `submission.csv`.\n",
                ],
            },
            _code_cell(_embed_cell(sources), "casmi-embed"),
            _code_cell(INFER_CELL, "casmi-infer"),
        ],
    }
    code_file = "casmi26-first-submission.ipynb"
    nb_path = KERNEL_DIR / code_file
    nb_path.write_text(json.dumps(nb, indent=1), encoding="utf-8")

    meta = {
        "id": "ilakkmanoharan/casmi26-retrieval-symbolic-v01",
        "title": "casmi26-retrieval-symbolic-v01",
        "code_file": code_file,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": False,
        "enable_tpu": False,
        "enable_internet": False,
        "dataset_sources": ["ilakkmanoharan/rdkit-cp312-wheels-casmi26"],
        "competition_sources": ["enveda-CASMI26-molecule-id-mass-spectra"],
        "kernel_sources": [],
        "model_sources": [],
    }
    (KERNEL_DIR / "kernel-metadata.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    return nb_path
