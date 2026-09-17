# Analysis — 2026-09-17 cycle05

## Quota (pre-flight, 2026-09-17 06:14 UTC / 01:14 America/Chicago)

Competition-day clock starts **01:00 America/Chicago**. This run is **14 minutes** into Chicago day 2026-09-17.

| Clock | Submissions counted | Remaining of 5 |
|-------|---------------------|----------------|
| **Chicago day** (since 2026-09-17 01:00 CDT = 06:00 UTC) | **0** in `agent/state.json`; no casmi-loop run after 06:00 UTC | **5** |
| **Kaggle UTC calendar day** (loop `submissions_on`) | **4** as of last successful Actions log (3 before cycle04 + new id `56290985`) | **1** |

**Decision:** quota is **not** exhausted. Proceed with one code submission (UTC slot 5 / tag `2026-09-17_cycle05`). Stop if a later Kaggle list shows 5.

Cloud Agent env has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` (confirmed empty; `~/.kaggle/kaggle.json` not written). Live `kaggle competitions submissions` could not be queried from this runner. Counts below are from GitHub Actions logs + committed `agent/state.json` + public leaderboard mirrors — **no invented scores**.

## Recent submissions (from casmi-loop logs + state)

| Kaggle id | When (UTC) | Message | Public score | Kernel |
|-----------|------------|---------|--------------|--------|
| 56253059 | 2026-09-15 | v0.1 retrieval+symbolic preferred-libs modified-cosine | **0.143** | v2 |
| 56258556 | 2026-09-15 | v0.2 ban-poisoned-exact-dup-IKs + entropy/modcos hybrid + all-libs | null | — |
| 56289779 | 2026-09-16 | probe v3 | null | — |
| 56289785 | 2026-09-16 | 2026-09-16 v10 rdkit-install fix + all-libs entropy/modcos | null | v10 |
| 56290242 | 2026-09-17 00:46 | Refining mass tolerance parameters… | null (PENDING at submit) | v11 |
| 56290985 | 2026-09-17 01:27 | Optimizing mass tolerance parameters… | null (PENDING at submit) | v12 |

`best_public_score` in state remains **0.143**. CLIST/Kaggle public LB still lists **Ilakk manoharan / ilakkmanoharan at ~0.14** (CLIST rank ~223, “5 hours ago”), consistent with only v0.1 having a published score.

Later kernel versions may still be pending or unscored in the public table.

## Leaderboard context (2026-09-17)

- Public LB top: **GUAM ~0.33–0.34** ([Kaggle leaderboard](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard); [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/)).
- Pack of teams at **0.30–0.32**. Gap vs us: roughly **2.3×**.
- Metric is public MRR@25 on ~33% of test.

## Why score is still low

1. **Poisoned exact duplicates (v0.1 root cause, still the best explanation for 0.143).** Local diagnostics: every molecule rank-1 sim=1.0 on `enveda-180` identical spectra whose train labels ≠ GT. Ban is on in current config (`EXCLUDE_EXACT_DUPLICATES=True`) but we have **no scored public number** confirming the ban helped.
2. **Cycles 03–04 only moved mass ppm** (5/10 then 10/15). That is a decoy-filter tweak, not a ranking-function change. If the remaining evidence after the dup-ban is near-isobar noise, ppm alone will not lift MRR.
3. **Entropy weight never landed.** Cycle02 specified `ENTROPY_WEIGHT=0.70`; kernel v4 **ERROR** (RDKit / poller). Current `casmi26/config.py` still has **0.55**. Hybrid is still close to 50/50 cosine.
4. **Cosine saturation on near-duplicates.** After dropping exact dups, modified cosine can still score structurally wrong isobars highly; entropy similarity is the literature-backed discriminator (Li 2021/2023).
5. Leaders at 0.33 imply methods beyond exact library cosine (embeddings, formula, or better re-rank). We stay in the retrieval+symbolic envelope this slot.

## Concrete improvement for this slot

- **One major ablation:** `ENTROPY_WEIGHT=0.70` (0.70·entropy + 0.30·modified cosine).
- Keep mass at cycle04 (`MASS_TOL_PPM=10`, `MASS_TOL_PPM_BACKFILL=15`) and keep the exact-dup ban.
- Next slots if this is flat: raise `TOP_K_SPECTRA_PER_QUERY` (multi-CE support) or lower `MIN_SIMILARITY` — not both at once.

## Submit attempt (this Cloud runner)

Tried `kaggle competitions submissions` and `kaggle kernels push -p kaggle_kernel`. Both stopped at **Authentication required** — `KAGGLE_USERNAME` / `KAGGLE_KEY` are not in this Cloud Agent environment, so `~/.kaggle/kaggle.json` was not written. **No kernel push and no `competition_submit_code` from this runner.** `gh workflow run casmi-loop.yml --ref cursor/competition-day-cycle-afdb -f slot=5` returned **HTTP 403** (resource not accessible by integration). Remaining submit path: merge PR #3 or run casmi-loop from a token that can dispatch Actions.

## Actions / runner notes

- Last casmi-loop success: run `35169491033` (2026-09-17 01:10 UTC) → cycle04, kaggle id 56290985.
- No in-progress/queued casmi-loop at 06:14 UTC.
- This Cloud Automation **cannot** call Kaggle until secrets are injected; GitHub Actions remains the laptop-off submit path.
