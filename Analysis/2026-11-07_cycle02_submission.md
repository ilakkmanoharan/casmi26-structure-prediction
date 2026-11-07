# Analysis — 2026-11-07 cycle02

## Quota (re-checked at 2026-11-07T06:00Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago**. At trigger time the Chicago clock is **00:02 CST** (still competition day **2026-11-06** until 07:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py` → `competition_day()` = **2026-11-07**).

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are unset in this Cloud env; `~/.kaggle/kaggle.json` was **not** written. Counts below come from GitHub Actions logs + `origin/main` `agent/state.json` (no secret values).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-07 | **1 / 5** | 4 | 58076904 (02:53Z, Actions 42330089426, kernel v202, `2026-11-07_cycle01 H-top-peaks`) |
| Chicago 01:00 window (since 2026-11-06 07:00Z) | **4 / 5** | 1 | 58055178, 58065731, **58071327** (cycle04 submit succeeded, git push to main failed), 58076904 |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off as `2026-11-07_cycle02` |

UTC slot 1 already used the no-op `TOP_PEAKS=128`. This cycle is UTC **slot 2**.

## Recent Kaggle submissions (newest first, from Actions logs)

- id=**58076904** score=None status=COMPLETE desc=`2026-11-07_cycle01 H-top-peaks` kernel **v202** (Actions 42330089426, 02:53Z) — **no-op** (`TOP_PEAKS` already 128)
- id=**58071327** score=None status=COMPLETE desc=`2026-11-06_cycle04 H-peaks` kernel **v201** (Actions 42307757034, 23:09Z) — submit ok, **git push to main failed** (`remote: Internal Server Error`); `TOP_PEAKS=160` was then overwritten by v202
- id=**58065731** score=None status=COMPLETE desc=`2026-11-06_cycle03 H-peak-mz` kernel **v200**
- id=**58055178** score=None status=COMPLETE desc=`2026-11-06_cycle02 H-peak-mz` kernel **v199**
- id=**58042294** score=None status=COMPLETE desc=`2026-11-06_cycle01 H-top-peaks` kernel **v198**
- id=58035989 / 58026170 / 58012064 — 2026-11-05 H-peak-mz / H-peak-mz / H-top-peaks

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~2026-11-07T02:00Z, ~4h stale)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.53**, **Oleksandr Parfionov 0.52**, **democat 0.51**, pikachu / Paweł Biernat / CHU1PC 0.50. Community analog/ensemble notebooks still ~0.43–0.48. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits. Remaining ranking must come from non-identical spectral evidence.

2. **The top-25 is still filled at hybrid ≥ 0.05.** `retrieve_for_spectrum` keeps every mass-window hit with `sim >= cfg.min_similarity` (`casmi26/retrieve.py`). Live `MIN_SIMILARITY=0.05` is an order of magnitude below Li/Fiehn’s FDR operating region. After the 0.02 Da pair window landed, more *pairs* match — including decoys — so a low floor now *amplifies* junk in the MRR@25 list.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-07 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `INTENSITY_FLOOR=0.01`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `TOP_K=120`, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-2 fallback) does not change the spectrum object or the rank list.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-2** fallback from already-live H-peak-mz to **H-sim-gate**, and stop slot-4’s fallback from resetting the floor back to 0.05 (`TOP_PEAKS=160` only).

If this PR is **not** merged before the next unused casmi-loop slot, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — another no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 2 can reuse them after merge.
