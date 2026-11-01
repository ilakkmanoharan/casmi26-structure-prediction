# Analysis 2026-11-01_cycle02

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC on 2026-11-01, CDT). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

## Quota (re-checked 06:04 UTC)

Cloud secrets `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent**, so `write_kaggle_credentials()` returned **False** and `~/.kaggle/kaggle.json` was not written. `kaggle competitions submissions` is not callable. Count is from `agent/state.json` + GitHub Actions `casmi-loop` + prior Cloud notes.

| Clock | Used | Remaining | Rows counted |
|-------|------|-----------|--------------|
| UTC calendar 2026-11-01 | **1/5** | 4 | Actions → Kaggle **57857604** H-top-peaks kernel v180 ~02:17Z (`TOP_PEAKS=128`, already live) |
| Chicago 01:00 (this prompt) | **0/5** | 5 | 57857604 landed *before* 06:00 UTC / 01:00 CDT |

Quota is **not** exhausted. This is the 01:00 CDT / 06:03 UTC slot (first suggested Cloud cadence). Next unused casmi-loop hourly is **07:00 UTC**.

Prior Cloud H-min-sim PRs **#38–#53** stayed draft/unmerged. Actions 10-31 later burned UTC tickets 2–5 on H-peak-mz / H-peaks / H-domain (already-live or no-op knobs). This cycle re-implements the first unused real ablation on current `main` after Actions 11-01 cycle01.

## Recent submissions (from committed Analysis + state)

- id=57857604 score=None status=COMPLETE desc=`2026-11-01_cycle01 H-top-peaks` (`TOP_PEAKS=128`, already live)
- id=57852239 score=None status=COMPLETE desc=`2026-10-31_cycle05 H-domain`
- id=57847630 score=None status=COMPLETE desc=`2026-10-31_cycle04 H-peaks`
- id=57840318 score=None status=COMPLETE desc=`2026-10-31_cycle03 H-peak-mz`
- id=57830376 score=None status=COMPLETE desc=`2026-10-31_cycle02 H-peak-mz`
- id=57821778 score=None status=COMPLETE desc=`2026-10-31_cycle01 H-top-peaks`

No scored public row above **0.143**. Kernel versions keep incrementing; public MRR does not.

## Leaderboard context (CLIST, updated ~13h before 06:04Z)

Savko **0.52**, Parfionov **0.52**, pikachu / Shehab / CHU1PC / democatXamer **0.50**. Community analog notebooks now badge **0.472–0.479** (`CASMI26 LB 0.479 | MIDX Exact Dedup Fill` is the current public-notebook high). Gap vs our 0.143 is analog + fingerprint + in-silico rerank, but the immediate no-op is that Actions will replay `PEAK_MZ_TOL=0.02` unless fallbacks are retargeted.

## Why score is low

1. **Exact test↔train spectrum duplicates** in `enveda-180` with train labels ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` already bans those inchikey14s. Remaining score is from non-identical evidence.

2. **Admission floor is 0.05.** `retrieve_for_spectrum` (`casmi26/retrieve.py`) keeps every hybrid entropy/modcos hit ≥ `cfg.min_similarity`. At 0.05, weak cross-library decoys fill `TOP_K_SPECTRA=120` and crowd the top-25. Literature identification floors are 0.55–0.75 (entropy), ~0.6 (MS2Query discard band), ~0.5 (GNPS cosine), or ~0.3 (loose cosine). 0.12 is the first unused one-knob step.

3. **Slot rotation is a no-op.** Live main after Actions 11-01 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Slot-2 and slot-3 fallbacks still apply `PEAK_MZ_TOL=0.02`. Slot-4 `H-peaks` currently sets `MIN_SIMILARITY=0.05`, which would undo a merged floor raise.

## Concrete improvement for this slot

**`MIN_SIMILARITY` 0.05 → 0.12** (library-hit admission floor).

Retarget Actions **slot-2 and slot-3** fallbacks to **H-min-sim**, and **slot-4** to `TOP_PEAKS=160` **without** resetting the floor.

If this PR is **not** merged before **07:00 UTC**, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

`write_kaggle_credentials()` returned **False**. No `kernels push` / `competition_submit_code` from Cloud. Do **not** dispatch casmi-loop until merged.
