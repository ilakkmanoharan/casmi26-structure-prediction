# Spec 2026-10-12_cycle02 — H-peak-mz

## Goal

One major ablation vs live `main` / 2026-10-12 cycle01 (`TOP_PEAKS=128`): set fragment matching to the MSEntropy library-search default **0.02 Da**. Retarget Actions slot-2 fallback so the next hourly `casmi-loop` does not waste UTC ticket 2/5 on already-applied `ENTROPY_WEIGHT=0.75`.

## Config patch (existing `casmi26/config.py` constants only)

```json
{"PEAK_MZ_TOL": 0.02}
```

`config_patch: {"PEAK_MZ_TOL": 0.02}`

Unchanged on purpose:

| Constant | Value | Why |
|----------|-------|-----|
| `EXCLUDE_EXACT_DUPLICATES` | `true` | Poisoned exact-dup guard |
| `ENTROPY_WEIGHT` | `0.75` | Already Li/Fiehn operating point |
| `TOP_PEAKS` | `128` | Cycle01 fragment ladder |
| `MASS_TOL_PPM` | `35.0` | Do not confound H1 |
| `MASS_TOL_PPM_BACKFILL` | `80.0` | Do not confound H1 |
| `INTENSITY_FLOOR` | `0.001` | Next unused lever |
| `MIN_SIMILARITY` | `0.05` | Do not stack H4 |

## Implementation steps

1. Set `PEAK_MZ_TOL = 0.02` in `casmi26/config.py`.
2. In `scripts/casmi_loop/chatgpt_spec.py`, replace `FALLBACK_ABLATIONS[1]` (H-entropy / `ENTROPY_WEIGHT=0.75`) with H-peak-mz / `PEAK_MZ_TOL=0.02`.
3. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. Tests: `PEAK_MZ_TOL == 0.02`; slot-2 fallback is H-peak-mz; existing TOP_PEAKS / ENTROPY_WEIGHT / credential tests still pass.
5. Submit path: `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never** CSV `competitions submit`.
6. If Cloud lacks Kaggle secrets: record skip, push artifacts, open PR so Actions (secrets present) can submit after merge.

## Submission message

`2026-10-12_cycle02 H-peak-mz (PEAK_MZ_TOL 0.01→0.02)`

## Success criteria

- Kernel metadata `enable_internet` is false.
- `PEAK_MZ_TOL == 0.02` in package and embedded notebook.
- Actions slot-2 fallback is H-peak-mz.
- Unit tests pass.
- Code submission created, **or** Analysis documents auth skip.
- `agent/state.json` appends this cycle.
