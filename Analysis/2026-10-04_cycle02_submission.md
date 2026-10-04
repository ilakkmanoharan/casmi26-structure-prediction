# Analysis — 2026-10-04 cycle02

## Quota (re-checked 2026-10-04T06:15Z)

- Competition day clock in `CLOUD_CYCLE_PROMPT.md`: day starts **01:00 America/Chicago**. Now = 01:15 CDT, so Chicago day **2026-10-04** is open.
- Actions `competition_day()` is **UTC calendar date** (see `scripts/casmi_loop/slots.py`). UTC day 2026-10-04 already has **1** recorded submit.
- **Could not call** `kaggle competitions submissions` — `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are absent in this Cloud env (`write_kaggle_credentials()` → False). Counts below are from committed `agent/state.json` + cycle01 analysis, not a live API list.

| Clock | Used / 5 | Evidence |
|-------|----------|----------|
| UTC (Kaggle reset) | **1 / 5** | `56815069` `2026-10-04_cycle01 H-top-peaks` at 05:21Z, kernel v54 |
| Chicago 01:00 | **0 / 5** | That submit is 00:21 CDT, **before** 01:00 CDT |

Quota is **not** exhausted. Proceed as `2026-10-04_cycle02`. Do **not** exit.

## Recent submissions (from cycle01 briefing + state.json)

All listed public scores are still **null** (Kaggle often lags; v0.1 0.143 remains the only scored public we trust).

| id | score | status | desc |
|----|-------|--------|------|
| 56815069 | None | COMPLETE | 2026-10-04_cycle01 H-top-peaks (`TOP_PEAKS=128`) |
| 56806727 | None | COMPLETE | 2026-10-03_cycle05 H-domain |
| 56803325 | None | COMPLETE | 2026-10-03_cycle04 H-peaks |
| 56798014 | None | COMPLETE | 2026-10-03_cycle03 H-mass-wide |
| 56791435 | None | COMPLETE | 2026-10-03_cycle02 H-entropy |
| 56785817 | None | COMPLETE | 2026-10-03_cycle01 H-top-peaks |

Best public in `agent/state.json`: **0.143**. Prize table (CLIST, ~2026-10-04T06:15Z): **pikachu 0.47**, Shehab / chopper / Randy **0.44**. Gap is analog / multi-channel ranking, not another 128-peak restore.

## Why score is low

1. **Poisoned exact-dup (v0.1).** Exact test↔train spectra in `enveda-180` with train labels ≠ GT. Perfect library match of those rows yields ~0.143. `EXCLUDE_EXACT_DUPLICATES=True` is on; we still cannot claim Class-3 de novo is solved.
2. **Cleaning mismatch vs entropy literature.** Live `INTENSITY_FLOOR=0.001` keeps ions at 0.1% of base peak. Flash / msentropy default is **1%**. After `TOP_PEAKS=128`, those noise rungs occupy greedy match slots and inflate hybrid similarity to the wrong inchikey14.
3. **Slot-2 fallback is a no-op.** `ENTROPY_WEIGHT` is already 0.75. If this PR is not merged before the next hourly `casmi-loop`, UTC slot 2 will resubmit H-entropy and waste a ticket.
4. **Unmerged Cloud PRs #13–#17** already specified this floor; Actions never picked them up.

## Concrete improvements for this slot

- **Do now:** `INTENSITY_FLOOR` 0.001 → **0.01**; retarget `FALLBACK_ABLATIONS[1]` from `H-entropy` to `H-intensity`.
- **Hold:** `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `TOP_K_SPECTRA_PER_QUERY=120`, `MIN_SIMILARITY=0.05`, exact-dup ban.
- **Next unused after this lands:** `PEAK_MZ_TOL` 0.02 (Flash default) or `MIN_SIMILARITY` 0.12 (Cloud PRs #11/#12).

## Submit path

Notebook-only: `kaggle kernels push` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV `competitions submit`.
