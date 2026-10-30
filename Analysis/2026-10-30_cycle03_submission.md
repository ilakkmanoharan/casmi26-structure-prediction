# Analysis — 2026-10-30 cycle03

## Quota (checked before any submit)

Competition day starts **01:00 America/Chicago** (06:00 UTC under CDT). Kaggle’s 5-submit reset is **midnight UTC**, so both clocks are reported.

| Clock | Used | Remaining | Notes |
|-------|------|-----------|--------|
| **UTC calendar 2026-10-30** | **2 / 5** | 3 | Binding Kaggle quota |
| **Chicago 01:00 clock** | **1 / 5** | 4 | Only submits after 06:00 UTC count |

Quota is **not** exhausted. This run is **cycle03**.

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset in this Cloud environment; `~/.kaggle/kaggle.json` was not written. Kaggle CLI 2.2.5 is installed but cannot authenticate. Submission list below is reconstructed from `agent/state.json` + GitHub Actions logs (run 41025442759), not a live `kaggle competitions submissions` call.

## Recent Kaggle submissions (newest first)

- id=**57799491** score=None status=COMPLETE/PENDING desc=`2026-10-30_cycle02 H-peak-mz` kernel **v172** (~08:36Z; Actions 41025442759). **Replay of already-live `PEAK_MZ_TOL=0.02`.**
- id=**57789094** score=None status=COMPLETE desc=`2026-10-30_cycle01 H-top-peaks` kernel **v171** (~02:00Z; Actions 40987360854). **Replay of already-live `TOP_PEAKS=128`.** Before Chicago 01:00, so it does not count on the Chicago clock.
- id=**57783593** score=None status=COMPLETE desc=`2026-10-29_cycle04 H-peaks` kernel **v170**
- id=57777563 score=None status=COMPLETE desc=`2026-10-29_cycle03 H-peak-mz`
- id=57767052 score=None status=COMPLETE desc=`2026-10-29_cycle02 H-peak-mz`
- id=57756058 score=None status=COMPLETE desc=`2026-10-29_cycle01 H-top-peaks`
- id=57750957 score=None status=COMPLETE desc=`2026-10-28_cycle04 H-peaks`

No scored public MRR is attached to any of these rows. Best known scored public remains **0.143** (v0.1).

## Leaderboard context

CLIST (page “updated 11 hours ago” at ~09:00Z): **[Oleksandr Parfionov 0.52](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/)**, **Savko 0.51**, **pikachu / Shehab Alshehabi / CHU1PC 0.50**, team051 / Paweł Biernat / JJ 0.49, then a long 0.48 band. Community analog notebooks still ~0.43–0.46; copied-notebook pile ~0.464. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live (`TOP_PEAKS=128` after today’s cycle01, `PEAK_MZ_TOL=0.02` replayed again as cycle02).

## Why score is still ~0.143

1. **Exact test↔train spectrum duplicates in `enveda-180`.** Train InChIKey labels on identical peak lists do **not** match competition GT. v0.1 hit ~0.143 despite perfect library match. `EXCLUDE_EXACT_DUPLICATES=True` stays on; retrieval still cannot claim Class-3 de novo.

2. **Weak library hits pad the top-25.** `retrieve.py` keeps every hybrid score `>= cfg.min_similarity` before truncating to `TOP_K_SPECTRA_PER_QUERY=120`. Live `MIN_SIMILARITY=0.05` is far below GNPS library-search / MASST admission defaults and far below Li/Fiehn’s 0.75 *call* threshold. Decoys occupy rank-list slots that MRR@25 then treats as plausible.

3. **Slot rotation has been a no-op for weeks, and it just happened again.** Live main after Actions 10-30 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `PEAK_MZ_TOL=0.02`, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-3 fallback, same as slot-2) does not change the spectrum object. Cloud PR **#45** (cycle02 H-min-sim) missed the 08:00 UTC merge window; Actions then spent UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`. If this PR is not merged before **10:00 UTC**, Actions will spend UTC ticket 3 the same way.

## Concrete improvement this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Hold every other live knob: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, exact-dup exclusion on.

Retarget Actions **slot-3** (next unused hourly, **10:00 UTC**) from already-live H-peak-mz to **H-min-sim**. Retarget **slot-2** the same way so future UTC days cannot replay `PEAK_MZ_TOL=0.02`. Retarget **slot-4** to `TOP_PEAKS=160` only so it does not reset `MIN_SIMILARITY` back to 0.05.

## Cloud submit status

No `kernels push` / `competition_submit_code` from Cloud (missing Kaggle secrets). Did **not** dispatch casmi-loop (unmerged dispatch would replay `PEAK_MZ_TOL=0.02` on main). Handoff is the substantial cycle03 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 3 can reuse them after merge.
