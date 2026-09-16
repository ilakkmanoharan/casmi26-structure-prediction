# Spec — next submission (2026-09-16 cycle01)

## Objective

Land a scored Kaggle **code** submission whose *one* ranking change vs the current `main` package (`ENTROPY_WEIGHT=0.55`, exact-dup ban on, all-libs) is an **entropy-dominant hybrid**. Repair the kernel poller so a worker ERROR cannot burn a 5-hour poll.

Notebook-only. Competition: `enveda-CASMI26-molecule-id-mass-spectra`. Kernel: `ilakkmanoharan/casmi26-retrieval-symbolic-v01`.

## Major ablation (one)

Raise entropy weight from 0.55 → **0.70**.

config_patch: {"ENTROPY_WEIGHT": 0.70}

## Constants to leave unchanged this slot

| Constant | Keep |
|----------|------|
| `EXCLUDE_EXACT_DUPLICATES` | `True` |
| `MASS_TOL_PPM` | `25.0` |
| `MASS_TOL_PPM_BACKFILL` | `60.0` |
| `PEAK_MZ_TOL` | `0.05` |
| `TOP_PEAKS` | `128` |
| `INTENSITY_FLOOR` | `0.001` |
| `TOP_K_SPECTRA_PER_QUERY` | `80` |
| `TOP_CANDIDATES_PER_SPECTRUM` | `50` |
| `MIN_SIMILARITY` | `0.08` |
| `MAX_CANDIDATES` | `25` |

## Supporting (non-scoring) implementation

1. Apply only the `config_patch` above to `casmi26/config.py`.
2. `scripts/casmi_loop/submit.py`: `normalize_kernel_status()` must map `KERNELWORKERSTATUS.ERROR` / `KernelWorkerStatus.ERROR` → `ERROR` and exit; do not busy-wait 5 h.
3. `scripts/casmi_loop/build_kernel.py`: before `from rdkit import Chem`, bootstrap RDKit via `pip install --no-index` against `ilakkmanoharan/rdkit-cp312-wheels-casmi26` if import fails. Keep `enable_internet: false`. Add stable notebook cell ids (nbformat 4.5).
4. Workflow: `PYTHONUNBUFFERED=1` on the slot step so poll lines appear in Actions logs.
5. Rebuild `kaggle_kernel/`; `kaggle kernels push -p kaggle_kernel`; poll until COMPLETE; `competition_submit_code` (never CSV submit).

## Acceptance

- Unit tests pass (adducts/submission + kernel-status + config entropy weight)
- Kernel metadata `enable_internet` is false
- No placeholders; ≤25 unique inchikey14 per molecule (runtime on Kaggle)
- If kernel ERROR: do **not** submit; record `skipped_reason` in `agent/state.json`
- New public score visible on Kaggle when COMPLETE

## Message string

`2026-09-16_cycle01 ENTROPY_WEIGHT=0.70 entropy-dominant hybrid`
