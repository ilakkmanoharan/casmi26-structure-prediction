# Spec 2026-10-09_cycle02 — 1% intensity floor

## Goal

One major ablation vs live `main` / 2026-10-09 cycle01: drop peaks below **1% of base peak** after max-normalization so entropy/modcos match the Li/Fiehn + MSEntropy cleaner. Retarget Actions slot-2 so the next hourly `casmi-loop` submits this factor instead of the live no-op `ENTROPY_WEIGHT=0.75`.

## Config patch (existing `casmi26/config.py` constants only)

```json
{"INTENSITY_FLOOR": 0.01}
```

config_patch: {"INTENSITY_FLOOR": 0.01}

Unchanged on purpose:

| Constant | Value | Why |
|----------|-------|-----|
| `EXCLUDE_EXACT_DUPLICATES` | `true` | Poisoned exact-dup guard |
| `TOP_PEAKS` | `128` | Already live; do not confound H1 |
| `ENTROPY_WEIGHT` | `0.75` | Already live; slot-2 no-op |
| `MASS_TOL_PPM` | `35.0` | Live mass-wide |
| `MASS_TOL_PPM_BACKFILL` | `80.0` | Live mass-wide |
| `TOP_K_SPECTRA_PER_QUERY` | `120` | Live mass-wide |
| `PEAK_MZ_TOL` | `0.01` | Next unused (PR #22); not this slot |
| `MIN_SIMILARITY` | `0.05` | Do not confound H1 |

## Implementation steps

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
3. In `scripts/casmi_loop/chatgpt_spec.py`: change `FALLBACK_ABLATIONS[1]` from H-entropy to H-intensity `{INTENSITY_FLOOR: 0.01}`.
4. Tests: `INTENSITY_FLOOR == 0.01`; slot-2 fallback is H-intensity; `clean_spectrum` drops sub-1% peaks.
5. Submit path: `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never** CSV `competitions submit`.
6. If Cloud lacks Kaggle secrets: record skip, push artifacts, open PR so Actions (secrets present) can submit after merge.

## Submission message

`2026-10-09_cycle02 H-intensity (INTENSITY_FLOOR 0.001→0.01)`

## Success criteria

- Kernel metadata `enable_internet` is false.
- `INTENSITY_FLOOR == 0.01` in package and embedded notebook.
- Unit tests pass.
- Code submission created, **or** Analysis documents quota/auth skip.
- `agent/state.json` appends this cycle.
