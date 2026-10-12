# Analysis 2026-10-12_cycle02

Competition day (Chicago 01:00): **2026-10-12**. Clock at analysis: 01:05 CDT / 06:05 UTC.

## Quota

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| Chicago 01:00 (CLOUD_CYCLE_PROMPT) | **0 / 5** | 5 | No submit since 2026-10-12T06:00Z |
| UTC calendar (Kaggle reset + Actions `competition_day()`) | **1 / 5** | 4 | Actions already spent the UTC-day first ticket |

Kaggle CLI/API could not be queried this run: `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are **absent** from the Cloud Agent environment (same failure as 2026-09-25 through 2026-10-11 Cloud crons). Counts below come from committed `agent/state.json` and the cycle01 analysis written after the live API pull.

## Recent submissions (from state + 2026-10-12_cycle01 API briefing)

| Kaggle id | When (UTC) | Chicago day | Message | Public score |
|-----------|------------|-------------|---------|--------------|
| 57090053 | 2026-10-12T00:41Z (kernel v87) | **2026-10-11** (19:41 CDT Oct 11) | `2026-10-12_cycle01 H-top-peaks` | still null / last scored **0.143** |
| 57084837 | 2026-10-11T20:23Z v86 | 2026-10-11 | H-peaks | null |
| 57078867 | 2026-10-11T15:48Z v85 | 2026-10-11 | H-mass-wide | null |
| 57068674 | 2026-10-11T08:51Z v84 | 2026-10-11 | H-entropy | null |
| 57058992 | 2026-10-11T02:00Z v83 | 2026-10-10 | H-top-peaks | null |

Actions tagged 57090053 as `2026-10-12_cycle01` because it uses the **UTC** date, not the Chicago 01:00 anchor. Under CLOUD_CYCLE_PROMPT that ticket belongs to the Oct 11 Chicago day (the fifth UTC-named “Oct 12 cycle01” is actually late Oct 11 local). Chicago-clock Oct 12 is still empty.

## Why the public score is still ~0.143

1. **Poisoned exact dups (v0.1).** Exact test↔train spectra in `enveda-180` have train InChIKeys that are **not** competition GT. A perfect library match of those rows scores ~0.143. `EXCLUDE_EXACT_DUPLICATES=True` is on; we must keep preferring non-identical evidence.
2. **Retrieval-only ceiling.** CLIST (fetched 2026-10-12T06:05Z): **MarvinTMB 0.48**, **pikachu 0.48**, **CHU1PC 0.48**, then 0.47 / 0.46 pack. Community analog + ICEBERG/GLACIER + PubChem-prior notebooks sit ~0.32–0.42. We are a library ranker, not a de novo / popularity engine.
3. **Actions slot 2 is a no-op.** Live `main` already has `ENTROPY_WEIGHT=0.75`. Every UTC afternoon Actions reapplies H-entropy and burns a ticket. Cloud draft PRs that retarget slot 2 (H-intensity / H-peak-mz, #13–#25) stay unmerged.
4. **Fragment match window is tighter than the literature default.** `PEAK_MZ_TOL=0.01` while MSEntropy search defaults to **0.02 Da** and Li/Fiehn 2021 matched at **0.05 Da**. True-structure peaks that centroid 0.012–0.019 Da apart never pair, so entropy/modcos under-ranks the correct IK14.

## Live `main` after Actions 10-12 cycle01 (kernel v87)

| Constant | Value |
|----------|-------|
| `TOP_PEAKS` | 128 |
| `ENTROPY_WEIGHT` | 0.75 |
| `MASS_TOL_PPM` / backfill | 35 / 80 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `PEAK_MZ_TOL` | **0.01** (unused lever) |
| `INTENSITY_FLOOR` | 0.001 (unused; draft PRs) |
| `EXCLUDE_EXACT_DUPLICATES` | true |

## Concrete improvement this slot

One major ablation: **`PEAK_MZ_TOL` 0.01 → 0.02** (H-peak-mz). Retarget Actions `FALLBACK_ABLATIONS[1]` from H-entropy → H-peak-mz so the next hourly `casmi-loop` spends UTC ticket 2/5 on this patch instead of a no-op 0.75 re-submit.

If Cloud still cannot `kernels push`, merge this PR before ~07–08 UTC or slot 2 wastes another ticket.

Prior Cloud H-peak-mz PRs #20 / #22 / #24 and H-intensity PRs #13–#19, #21, #23, #25 remain draft/unmerged.
