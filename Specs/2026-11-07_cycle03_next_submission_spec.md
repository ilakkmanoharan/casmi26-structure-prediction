# Spec 2026-11-07_cycle03

One major ablation vs the last submitted kernel (v203, no-op `PEAK_MZ_TOL=0.02`).

## Hypothesis

`H-precursor-cut` — drop precursor-window ions using the ms_entropy / Flash Entropy cutoff.

## config_patch

```json
{"MAX_PEAKS_ABOVE_PRECURSOR_DA": -1.6}
```

Meaning: keep peaks with `mz <= precursor_mz - 1.6`.

## Code (required — the constant was previously unused)

1. `casmi26/config.py`
   - `MAX_PEAKS_ABOVE_PRECURSOR_DA = -1.6`
   - `RunConfig.max_peaks_above_precursor_da` defaults to that constant.
2. `casmi26/spectrum.py`
   - `clean_spectrum(..., remove_above_precursor_da=-1.6)` default.
3. Pass `remove_above_precursor_da=cfg.max_peaks_above_precursor_da` from:
   - `casmi26/index.py` (library index)
   - `casmi26/retrieve.py` (poisoned-dup scan, per-query retrieval, backfill)
4. Rebuild `kaggle_kernel/` with `enable_internet: false` and RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
5. Slot-3 fallback in `scripts/casmi_loop/chatgpt_spec.py` becomes this patch so unattended Actions does not re-apply `PEAK_MZ_TOL=0.02`.

Do **not** change `TOP_PEAKS`, `PEAK_MZ_TOL`, `ENTROPY_WEIGHT`, `MIN_SIMILARITY`, or mass ppm in this kernel.

## Submit

- Kernel: `ilakkmanoharan/casmi26-retrieval-symbolic-v01`
- `kaggle kernels push -p kaggle_kernel`
- Poll until COMPLETE
- `competition_submit_code` only (never CSV)
- Message: `2026-11-07_cycle03 H-precursor-cut`

## Acceptance

- Unit tests: precursor-window ions dropped; `RunConfig` wires −1.6; slot-3 fallback is `H-precursor-cut`.
- Embedded notebook source contains `MAX_PEAKS_ABOVE_PRECURSOR_DA = -1.6` and the wired `clean_spectrum` calls.
- One Kaggle **code** submission, or an explicit skip if quota/credentials block it.
