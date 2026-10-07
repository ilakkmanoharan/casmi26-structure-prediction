# Analysis 2026-10-07_cycle02

## Quota (re-checked 2026-10-07T06:05Z)

Competition day starts **01:00 America/Chicago** (06:00 UTC). Cloud Automation
**does not receive** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so
the Kaggle submissions API could not be queried from this runner.

Inferred from committed `agent/state.json`:

| Clock | Count | Evidence |
|-------|-------|----------|
| Chicago 01:00 | **0 / 5** | Only Oct-7 cycle so far is Actions `56895779` at **00:51Z** (19:51 CDT Oct 6) — *before* day start. |
| UTC calendar 2026-10-07 | **1 / 5** | Same `56895779` H-top-peaks, kernel v66. |

**Not exiting for quota.** Chicago-clock slot 2 is free. If credentials appear,
submit this cycle. Otherwise merge this branch before the next hourly
`casmi-loop` so UTC slot 2 does not burn another ticket on live no-op
`ENTROPY_WEIGHT=0.75`.

## Score context

- Our best **scored** public MRR@25 remains **0.143** (v0.1). Later complete
  submits (`56866331` … `56895779`) still show `publicScore=None` in Actions
  logs — Kaggle often delays the public number, but nothing has beaten 0.143
  in committed state.
- CLIST prize table (fetched 2026-10-07T06:05Z): **pikachu 0.48**, MarvinTMB
  0.47, then Oliver Ford / vukpetar 0.45, then a 0.44 pack (Nicolas, Sho,
  Sls2, Arsokan, Bertan, Shehab, Randy, chopper, Xolotl, Baligh).
  https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/
- Public analog / quad-channel notebooks still cluster **0.328–0.339**.

## Why 0.143 is stuck

1. **Poisoned exact dups** in `enveda-180`: test↔train spectra match, train
   labels ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=true` is already on.
2. **Actions fallbacks are live no-ops.** Slot 1 `TOP_PEAKS=128`, slot 2
   `ENTROPY_WEIGHT=0.75`, slot 3 mass-wide 35/80 + `TOP_K=120` are already
   the values on `main` (`casmi26/config.py`). Repeating them cannot move MRR.
3. **Cleaning is too permissive.** `INTENSITY_FLOOR=0.001` keeps 0.1%
   relative ions after max-normalization. Those ions participate in greedy
   m/z matching for both entropy and modified cosine, inflating support for
   wrong structures. Literature 1–2% intensity denoising is the unused lever.
4. Cloud H-intensity PRs **#13–#19** and H-peak-mz **#20** never merged, so
   `PEAK_MZ_TOL` is still 0.01 and the floor is still 0.001.

## Next slot

One major factor vs live main: **`INTENSITY_FLOOR` 0.001 → 0.01**.
Retarget Actions slot-2 fallback from H-entropy to **H-intensity** so the
OpenAI-missing path cannot re-submit 0.75.
