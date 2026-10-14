# Analysis 2026-10-14_cycle02

Competition day starts 01:00 America/Chicago (06:00 UTC). Cloud Automation cron fired 2026-10-14T06:04:59Z (01:04 CDT).

## Quota

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| Chicago 01:00 (CLOUD_CYCLE_PROMPT) | **0/5** at cycle start | 5 | First Chicago-day slot. |
| UTC calendar (Kaggle + Actions `competition_day()`) | **1/5** | 4 | Actions 38493019853 → Kaggle **57162467** kernel v94 `2026-10-14_cycle01 H-top-peaks` at 01:21Z (20:21 CDT Oct 13, still previous Chicago day). |
| In flight | Actions **38519649255** `in_progress` since 05:59Z | — | Hourly casmi-loop on main; will likely spend UTC slot 2 on fallback `H-entropy` / `ENTROPY_WEIGHT=0.75` (already live). |

Kaggle CLI list was **not** available: `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are absent in this Cloud environment (same failure as 2026-09-25/26 and every later Cloud cron). Quota above is from `agent/state.json` + `gh run list` + the cycle01 analysis briefing.

**Not a 5/5 skip.** Do not exit; implement H-intensity and hand off to Actions.

## Recent submissions (from cycle01 briefing + state)

- id=57162467 score=None status=COMPLETE desc=2026-10-14_cycle01 H-top-peaks (kernel v94)
- id=57156600 score=None status=COMPLETE desc=2026-10-13_cycle04 H-peaks
- id=57149351 score=None status=COMPLETE desc=2026-10-13_cycle03 H-mass-wide
- id=57135691 score=None status=COMPLETE desc=2026-10-13_cycle02 H-entropy
- id=57124847 score=None status=COMPLETE desc=2026-10-13_cycle01 H-top-peaks
- id=57114938 score=None status=COMPLETE desc=2026-10-12_cycle03 H-mass-wide
- id=57099716 score=None status=COMPLETE desc=2026-10-12_cycle02 H-entropy
- id=57090053 score=None status=COMPLETE desc=2026-10-12_cycle01 H-top-peaks

All public scores still **null**. Best scored public remains **0.143** (v0.1). Live LB top **CHU1PC 0.491** (2026-10-14T06:07Z).

## Why the score is low

1. **Poisoned exact duplicates.** Test spectra that are byte-identical to `enveda-180` train rows carry train InChIKeys that do **not** match competition GT. Perfect library match → ~0.143 public. Guard is on (`EXCLUDE_EXACT_DUPLICATES=True`); remaining lift must come from non-identical evidence.
2. **Actions fallbacks are no-ops on live main.** After cycle01, `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80 + `TOP_K=120`, `MIN_SIMILARITY=0.05`. Slot 2–5 fallbacks re-apply those same values. The 06:00 UTC run will waste a ticket if it submits H-entropy again.
3. **Noise floor is 10× too low vs literature.** `INTENSITY_FLOOR=0.001` keeps 0.1% base-peak ions. Flash Entropy / matchms drop ions below **1%**. Those junk peaks occupy the 128-peak ladder and inflate entropy matches to decoys.
4. **Leaderboard gap is analogue / forward, not another mass window.** Top public 0.45–0.49 uses analogue expansion and simulated spectra. Retrieval-only cannot claim Class-3 de novo.

## What to change this slot

One major unused constant: **`INTENSITY_FLOOR` 0.001 → 0.01**.

Do not resubmit H-entropy, H-mass-wide, or H-top-peaks. Next unused after this: `PEAK_MZ_TOL` 0.02 (draft PRs #20/#22/#24/#26) or `MIN_SIMILARITY` 0.12 (PRs #11/#12).

## Cloud submit blocker

Cannot `kernels push` / `competition_submit_code` without Kaggle secrets. Commit substantial cycle02 docs + config + slot-2 fallback retarget so the next casmi-loop on a merged main reuses `config_patch: {"INTENSITY_FLOOR": 0.01}` instead of `ENTROPY_WEIGHT=0.75`.
