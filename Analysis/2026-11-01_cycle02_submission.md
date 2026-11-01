# Analysis 2026-11-01_cycle02

Competition day for this Cloud prompt starts **01:00 America/Chicago**. On 2026-11-01 that first occurred at **06:00 UTC** (01:00 CDT). US DST then ended at 02:00 CDT → 01:00 CST. This late `0 6 * * *` cron fired at **07:34 UTC / 01:34 CST**. Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

## Quota (re-checked 07:36 UTC)

Cloud secrets `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent**, so `write_kaggle_credentials()` returned **False** and `~/.kaggle/kaggle.json` was not written. `kaggle competitions submissions` is not callable. Count is from `agent/state.json` + GitHub Actions `casmi-loop` + public CLIST / prior Cloud notes.

| Clock | Used | Remaining | Rows counted |
|-------|------|-----------|--------------|
| UTC calendar 2026-11-01 | **1/5** | 4 | Actions run `41263245036` → Kaggle **57857604** H-top-peaks kernel v180 ~02:17Z (`TOP_PEAKS=128`, already live) |
| Chicago 01:00 (this prompt) | **0/5** | 5 | 57857604 landed *before* 06:00 UTC / first 01:00 CDT |

Quota is **not** exhausted. Next unused cycle on `main` is **cycle02**. Cloud PR **#54** already wrote cycle02 at 06:03Z but stayed draft. 07:00 UTC `casmi-loop` did **not** fire (last success is still 01:58Z). Next unused casmi-loop hourly is **08:00 UTC**.

Prior Cloud H-min-sim PRs **#38–#54** stayed draft/unmerged. Actions 10-31 later burned UTC tickets 2–5 on H-peak-mz / H-peaks / H-domain (already-live or no-op knobs). This late re-fire re-implements the first unused real ablation on current `main` after Actions 11-01 cycle01.

## Recent submissions (from committed Analysis + state)

- id=57857604 score=None status=COMPLETE desc=`2026-11-01_cycle01 H-top-peaks` (`TOP_PEAKS=128`, already live)
- id=57852239 score=None status=COMPLETE desc=`2026-10-31_cycle05 H-domain`
- id=57847630 score=None status=COMPLETE desc=`2026-10-31_cycle04 H-peaks`
- id=57840318 score=None status=COMPLETE desc=`2026-10-31_cycle03 H-peak-mz`
- id=57830376 score=None status=COMPLETE desc=`2026-10-31_cycle02 H-peak-mz`
- id=57821778 score=None status=COMPLETE desc=`2026-10-31_cycle01 H-top-peaks`

No scored public row above **0.143**. Kernel versions keep incrementing; public MRR does not.

## Leaderboard context (CLIST, updated ~15h before 07:36Z)

Savko **0.52**, Parfionov **0.52**, pikachu / Shehab / CHU1PC / democatXamer **0.50**. Community analog notebooks still badge **0.479** (`CASMI26 LB 0.479 | MIDX Exact Dedup Fill`; Flexonafft V56 also 0.479). Gap vs our 0.143 is analog + fingerprint + in-silico rerank, but the immediate no-op is that Actions will replay `PEAK_MZ_TOL=0.02` unless fallbacks are retargeted.

## Why score is low

1. **Exact test↔train spectrum duplicates** in `enveda-180` with train labels ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` already bans those inchikey14s. Remaining score is from non-identical evidence.

2. **Admission floor is 0.05.** `retrieve_for_spectrum` (`casmi26/retrieve.py`) keeps every hybrid entropy/modcos hit ≥ `cfg.min_similarity`. At 0.05, weak cross-library decoys fill `TOP_K_SPECTRA=120` and crowd the top-25. Literature identification floors are 0.55–0.75 (entropy), ~0.6 (MS2Query discard band), ~0.5 (GNPS cosine). 0.12 is the first unused one-knob step.

3. **Slot rotation is a no-op.** Live main after Actions 11-01 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Slot-2 and slot-3 fallbacks still apply `PEAK_MZ_TOL=0.02`. Slot-4 `H-peaks` currently sets `MIN_SIMILARITY=0.05`, which would undo a merged floor raise.

## Concrete improvement for this slot

**`MIN_SIMILARITY` 0.05 → 0.12** (library-hit admission floor).

Retarget Actions **slot-2 and slot-3** fallbacks to **H-min-sim**, and **slot-4** to `TOP_PEAKS=160` **without** resetting the floor.

If this PR is **not** merged before **08:00 UTC**, the next unused `casmi-loop` hour will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

`write_kaggle_credentials()` returned **False**. No `kernels push` / `competition_submit_code` from Cloud. Do **not** dispatch casmi-loop until merged.
