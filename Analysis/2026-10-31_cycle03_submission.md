# Analysis 2026-10-31_cycle03

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC on 2026-10-31, CDT). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

## Quota (re-checked 12:04 UTC)

Cloud secrets `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent**, so `write_kaggle_credentials()` cannot write `~/.kaggle/kaggle.json`. `kaggle competitions submissions` is not callable. Count is from `agent/state.json` + GitHub Actions `casmi-loop` + prior Cloud notes.

| Clock | Used | Remaining | Rows counted |
|-------|------|-----------|--------------|
| UTC calendar 2026-10-31 | **2/5** | 3 | Actions 41150722176 → Kaggle **57821778** H-top-peaks kernel v175 ~00:44Z; Actions 41177934115 → Kaggle **57830376** H-peak-mz kernel v176 ~07:05Z |
| Chicago 01:00 (this prompt) | **1/5** | 4 | Only 57830376 is after 06:00 UTC |

Quota is **not** exhausted. 07:00, 08:00, 09:00, 10:00, 11:00, and **12:00** UTC casmi-loop hours did **not** fire. Next unused hourly is **13:00 UTC**.

Cloud cycle02 PR #49 (06:06Z H-min-sim) stayed draft; Actions then burned UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`. Cloud cycle03 PRs #50 (07:36Z), #51 (09:07Z), and #52 (10:36Z) are still draft/unmerged. This 12:03Z 07:00 CDT slot re-implements the same unused ablation on current `main`.

## Recent submissions (from committed Analysis + state)

- id=57830376 score=None status=COMPLETE desc=`2026-10-31_cycle02 H-peak-mz` (`PEAK_MZ_TOL=0.02`, already live)
- id=57821778 score=None status=COMPLETE desc=`2026-10-31_cycle01 H-top-peaks` (`TOP_PEAKS=128`, already live)
- id=57816688 score=None status=COMPLETE desc=`2026-10-30_cycle04 H-peaks`
- id=57810528 score=None status=COMPLETE desc=`2026-10-30_cycle03 H-peak-mz`
- id=57799491 score=None status=COMPLETE desc=`2026-10-30_cycle02 H-peak-mz`
- id=57789094 score=None status=COMPLETE desc=`2026-10-30_cycle01 H-top-peaks`

No scored public row above **0.143**. Kernel versions keep incrementing; public MRR does not.

## Leaderboard context (CLIST, updated ~15h before 12:04Z)

Parfionov **0.52**, Savko **0.52**, pikachu / Shehab / CHU1PC **0.50**. Community analog notebooks still badge **0.456–0.477** (`CASMI26 LB 0.477` is the current public-notebook high). Gap vs our 0.143 is analog + fingerprint + in-silico rerank, but the immediate no-op is that Actions will replay `PEAK_MZ_TOL=0.02` unless fallbacks are retargeted.

## Why score is low

1. **Exact test↔train spectrum duplicates** in `enveda-180` with train labels ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` already bans those inchikey14s. Remaining score is from non-identical evidence.

2. **Admission floor is 0.05.** `retrieve_for_spectrum` (`casmi26/retrieve.py`) keeps every hybrid entropy/modcos hit ≥ `cfg.min_similarity`. At 0.05, weak cross-library decoys fill `TOP_K_SPECTRA=120` and crowd the top-25. Literature identification floors are 0.55–0.75 (entropy), ~0.6 (MS2Query discard band), or ~0.3 (cosine). 0.12 is the first unused one-knob step.

3. **Slot rotation is a no-op.** Live main after Actions 10-31 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Slot-2 and slot-3 fallbacks still apply `PEAK_MZ_TOL=0.02`. Slot-4 `H-peaks` currently sets `MIN_SIMILARITY=0.05`, which would undo a merged floor raise.

## Concrete improvement for this slot

**`MIN_SIMILARITY` 0.05 → 0.12** (library-hit admission floor).

Retarget Actions **slot-2 and slot-3** fallbacks to **H-min-sim**, and **slot-4** to `TOP_PEAKS=160` **without** resetting the floor.

If this PR is **not** merged before **13:00 UTC**, Actions will spend UTC ticket 3 on `PEAK_MZ_TOL=0.02` — a third no-op today.

`write_kaggle_credentials()` returned **False**. No `kernels push` / `competition_submit_code` from Cloud. Do **not** dispatch casmi-loop until merged.
