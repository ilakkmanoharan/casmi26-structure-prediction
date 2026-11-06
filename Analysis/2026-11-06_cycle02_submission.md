# Analysis — 2026-11-06 cycle02

Cloud Automation `0 6 * * *` fired late at **2026-11-06T10:30:48Z** (04:30 CST). Chicago day start is 01:00 America/Chicago.

## Quota (not exhausted — do not skip implement)

`write_kaggle_credentials()` returned **False**: env has no `KAGGLE_USERNAME`, `KAGGLE_KEY`, or `KAGGLE_API_TOKEN`. `~/.kaggle/` exists and is empty. Live `kaggle competitions submissions` is impossible from this pod.

Proxy count from `agent/state.json` + `gh run list --workflow=casmi-loop.yml`:

| Clock | Submits counted | Limit | Remaining |
|-------|-----------------|-------|-----------|
| **UTC calendar 2026-11-06** (Kaggle reset; Actions `slots.py`) | **1/5** | 5 | 4 |
| **Chicago 01:00 2026-11-06** (CLOUD_CYCLE_PROMPT) | **0/5** | 5 | 5 |

Only UTC slot 1 exists: Actions [42147867834](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/42147867834) → Kaggle **58042294**, kernel **v198**, `H-top-peaks` (`TOP_PEAKS=128`) at 02:22Z. That stamp is **20:22 CST 2026-11-05**, so it does **not** count against the Chicago 01:00 day. Binding Kaggle limit is still UTC, so treat remaining tickets as **4**.

Hourly `casmi-loop` **03:00–10:00 UTC did not appear** in `gh run list` (last success 02:03Z). Draft Cloud PRs #77 (06:04Z), #78 (07:35Z), and #79 (09:05Z) already specified H-sim-gate and stayed **unmerged**, so Actions never applied it. The 09:01Z draft asked to merge before ~10:00 UTC; that hourly stayed dark, so UTC ticket 2 is still unused.

**Decision:** quota is not exhausted. Continue Research → Hypothesis → Spec → implement. Cannot `kernels push` / `competition_submit_code` from Cloud. Handoff: substantial cycle02 docs + fallback retarget so the next `casmi-loop` hour after merge submits this ablation instead of another `PEAK_MZ_TOL=0.02` no-op.

## Recent public scores (from committed Analysis + state)

Best **scored** public on this kernel family remains **0.143** (`agent/state.json` `best_public_score`). Recent Actions rows in cycle01 analysis still show `publicScore=None` at list time (Kaggle often lags):

- 58042294 2026-11-06_cycle01 H-top-peaks (v198)
- 58035989 2026-11-05_cycle03 H-peak-mz (v197)
- 58026170 2026-11-05_cycle02 H-peak-mz (v196)
- 58012064 2026-11-05_cycle01 H-top-peaks (v195)
- 58001652 2026-11-04_cycle04 H-peaks (v194)

Weeks of H-top-peaks / H-peak-mz / H-peaks rotation have not moved the scored public number. Replaying those live constants cannot be the next experiment.

## Leaderboard context

Live Kaggle CLIST / leaderboard fetch from this pod was rate-limited (`Too many requests`). Last Cloud-cycle memory (09:01Z, ~1.5 h stale at write time): Shehab Alshehabi **0.54**, Savko **0.53**, Parfionov **0.52**. Independent Oct-24 public dump put a large cluster at **0.464** (copied notebooks) and a thin tail above 0.47; a later community dump still listed pikachu ~0.50. Gap from 0.143 to ~0.50 is Class-1 retrieval vs Class-2 candidate generation (formula / fingerprint / analogue / in-silico frag). Retrieval alone does not close that gap.

## Why score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies in `enveda-180` carry train labels that are **not** competition GT. Perfect library match on those rows scores ~0.143, not 1.0. `EXCLUDE_EXACT_DUPLICATES=True` is already live; do not turn it off.

2. **Admission floor is noise.** `MIN_SIMILARITY=0.05` lets almost any mass-isobar with a shared ion into the 120-neighbor list. After 20 mDa pairing, those weak hits are *more* numerous, not fewer. MRR@25 then ranks decoys ahead of the true structure’s 2nd–5th spectrum. Li/Fiehn’s FDR work and MS2Query’s discard-below-0.6 practice both argue the live floor is far too low.

3. **Slot rotation is a no-op.** Live main after cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `INTENSITY_FLOOR=0.01`, `ENTROPY_WEIGHT=0.75`, `MASS_TOL_PPM=35`, `MIN_SIMILARITY=0.05`. Actions slot-2 and slot-3 fallbacks are still `{PEAK_MZ_TOL: 0.02}`. The next unused UTC ticket on current main would replay Flash Entropy pairing.

4. **Class-2/3 ceiling.** Public 0.46–0.54 methods add structure databases + in-silico scores. This kernel is retrieval over train libraries. Do not claim de novo.

## Concrete improvement for this slot

**One major change:** `MIN_SIMILARITY` **0.05 → 0.12**.

Also retarget Actions slot-2 and slot-3 fallbacks to `{MIN_SIMILARITY: 0.12}` so an OpenAI-429 / no-key hourly cannot waste UTC tickets 2–3 on live `PEAK_MZ_TOL`. Slot-4 keeps `{TOP_PEAKS: 160, MIN_SIMILARITY: 0.05}` as a later contrast (more peaks, *lower* gate).

Merge this branch before the next unused `casmi-loop` hour (**~11:00 UTC** if the 10:00 cron stays dark) so `write_cycle_docs` reuses these substantial files.
