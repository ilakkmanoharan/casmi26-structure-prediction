# Spec 2026-09-25_cycle01 — restore fragment ladder

## Goal

One major ablation vs `main` / 2026-09-17 cycle05: keep **128** cleaned peaks per spectrum so entropy/modcos can use a real fragment ladder. Unblock `casmi-loop` so a 429 from OpenAI does not abort the slot.

## Config patch (existing `casmi26/config.py` constants only)

```json
{"TOP_PEAKS": 128}
```

Unchanged on purpose:

| Constant | Value | Why |
|----------|-------|-----|
| `EXCLUDE_EXACT_DUPLICATES` | `true` | Poisoned exact-dup guard |
| `ENTROPY_WEIGHT` | `0.6` | Do not confound H1 |
| `MASS_TOL_PPM` | `10` | Cycle05 setting |
| `MASS_TOL_PPM_BACKFILL` | `15` | Cycle05 setting |
| `PEAK_MZ_TOL` | `0.01` | Cycle05 setting |
| `MIN_SIMILARITY` | `0.08` | Cycle05 setting |

`config_patch: {"TOP_PEAKS": 128}`

## Implementation steps

1. Set `TOP_PEAKS = 128` in `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
3. In `scripts/casmi_loop/chatgpt_spec.py`: catch OpenAI HTTP 429/5xx and network errors; slot-1 fallback = `{TOP_PEAKS: 128}`.
4. In `scripts/casmi_loop/submit.py`: `write_kaggle_credentials()` → `~/.kaggle/kaggle.json` mode 0600 + `access_token` (kaggle 2.2).
5. Tests: peak-count behavior, slot-1 fallback, 429 → `None`, credential file mode.
6. Submit path: `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never** CSV `competitions submit`.
7. If Cloud lacks Kaggle secrets: record skip, push artifacts, open PR so Actions (secrets present) can submit after the 429 fix.

## Submission message

`2026-09-25_cycle01 restore TOP_PEAKS 5→128 (entropy/modcos fragment ladder)`

## Success criteria

- Kernel metadata `enable_internet` is false.
- `TOP_PEAKS == 128` in package and embedded notebook.
- Unit tests pass.
- Code submission created, **or** Analysis documents quota/auth skip.
- `agent/state.json` appends this cycle.
