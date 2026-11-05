# Analysis — 2026-11-05 cycle02

## Quota (re-checked at 2026-11-05T12:04Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (07:00 UTC on CST). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`. `write_kaggle_credentials()` returned **False**; `~/.kaggle/kaggle.json` was **not** written. Counts below come from `gh run list` + `origin/main` `agent/state.json` after the 06:06Z Actions push (`8c9adc0`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-05 | **1 / 5** | 4 | 58012064 at 06:06Z (Actions 41976074079, kernel v195, `H-top-peaks`) |
| Chicago 01:00 (since 07:00 UTC) | **0 / 5** | 5 | The UTC ticket landed at 00:06 CST, *before* 01:00 CST |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

`casmi-loop` hourly after 05:46Z **did not fire** (07:00 / 08:00 / 09:00 / 10:00 / 11:00 / 12:00 UTC missing). Next unused Actions hour after this write is ~13:00 UTC.

## Recent Kaggle submissions (newest first, from Actions logs + state.json)

- id=**58012064** score=None status=COMPLETE desc=`2026-11-05_cycle01 H-top-peaks` kernel **v195** (Actions 41976074079, 06:06Z) — `TOP_PEAKS=128`
- id=**58001652** score=None status=COMPLETE desc=`2026-11-04_cycle04 H-peaks` kernel **v194**
- id=**57992996** score=None status=COMPLETE desc=`2026-11-04_cycle03 H-peak-mz` kernel **v193**
- id=**57979390** score=None status=COMPLETE desc=`2026-11-04_cycle02 H-peak-mz` kernel **v192**
- id=**57967804** score=None status=COMPLETE desc=`2026-11-04_cycle01 H-top-peaks` kernel **v191**
- id=57961369 score=None status=COMPLETE desc=`2026-11-03_cycle04 H-peaks`
- id=57953771 score=None status=COMPLETE desc=`2026-11-03_cycle03 H-peak-mz`
- id=57939381 score=None status=COMPLETE desc=`2026-11-03_cycle02 H-peak-mz`
- id=57927482 score=None status=COMPLETE desc=`2026-11-03_cycle01 H-top-peaks`
- id=57917568 score=None status=COMPLETE desc=`2026-11-02_cycle03 H-peak-mz`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1 exact-dup trap).

## Leaderboard context (CLIST ~2026-11-05T08:00Z, ~4 h stale)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.52**, **Oleksandr Parfionov 0.52**, **democat 0.51**, pikachu / Paweł Biernat / CHU1PC **0.50**. Native Kaggle `/leaderboard` returned HTTP 429 from this runner. Community analog/fusion notebooks still cluster ~0.46–0.50. Gap vs 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **The admission floor is still a near-zero noise gate.** `casmi26/retrieve.py` keeps every hybrid score `>= cfg.min_similarity` (currently **0.05**) before taking the top-120 spectra. After Flash Entropy 20 mDa pairing and the 128-peak ladder, many isobaric decoys clear 0.05 on a couple of shared mid-intensity ions and crowd the 25-SMILES list. Li 2021's 0.75 identity cutoff is too harsh for this hybrid; Flash Entropy's documented 0.01 example is too loose now that pairing is correct.

3. **Slot rotation has been a no-op for days.** Live main after Actions 11-05 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, `PEAK_MZ_TOL=0.02`, mass-wide 35/80, `TOP_K=120`, **`MIN_SIMILARITY=0.05`**. Slot-2/3 fallbacks still replay `PEAK_MZ_TOL=0.02`. Cloud H-min-sim drafts **#62–#75** and H-entropy-pure **#73** stayed unmerged.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-2** and **slot-3** fallbacks from already-live H-peak-mz to **H-min-sim**. Keep slot-4's extra-peaks tweak but pin `MIN_SIMILARITY=0.12` so it does not undo the floor.

If this PR is **not** merged before the next unused hourly (~13:00 UTC), Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — another no-op.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 2 can reuse them after merge.
