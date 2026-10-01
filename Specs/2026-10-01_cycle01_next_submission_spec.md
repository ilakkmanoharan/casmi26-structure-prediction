# Spec 2026-10-01_cycle01 — H-intensity (INTENSITY_FLOOR 0.01)

## Goal

One major ablation vs `main` @ `1281b82` / last Actions submit **56721177** (`H-domain`, kernel v40): align spectrum cleaning with the Li/Fiehn + msentropy **1%** noise floor.

## config_patch

```json
{"INTENSITY_FLOOR": 0.01}
```

config_patch: {"INTENSITY_FLOOR": 0.01}

## Unchanged (already live on main; do not confound H1)

| Constant | Value |
|----------|-------|
| `TOP_PEAKS` | 160 |
| `ENTROPY_WEIGHT` | 0.75 |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `PEAK_MZ_TOL` | 0.01 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
3. Retarget `FALLBACK_ABLATIONS[0]` from `H-top-peaks` (already live; would only shuffle 160→128) to `H-intensity` so the next unused UTC `casmi-loop` slot applies this patch if OpenAI is missing / 429 and Grok docs are not yet on main.
4. Tests: intensity-floor constant, slot-1 fallback, `clean_spectrum` drops a 0.5% peak at 0.01 and keeps it at 0.001. Relax the stale `TOP_PEAKS == 128` assertion (`main` is 160).
5. Submit path: `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never** CSV `competitions submit`.
6. If Cloud lacks Kaggle secrets: record skip, push artifacts, open PR so Actions (secrets present) can submit after merge. **Merge before the next hourly casmi-loop** or slot 1 wastes a ticket on `TOP_PEAKS=128`.

## Submission message

`2026-10-01_cycle01 H-intensity (INTENSITY_FLOOR 0.001→0.01)`

## Success criteria

- Kernel metadata `enable_internet` is false.
- `INTENSITY_FLOOR == 0.01` in package and embedded notebook.
- Unit tests pass.
- Code submission created, **or** Analysis documents quota/auth skip.
- `agent/state.json` appends this cycle.
