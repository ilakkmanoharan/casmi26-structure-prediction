# Analysis — 2026-09-16 cycle01

Competition day **2026-09-16** (anchor 01:00 America/Chicago / CDT). This Cloud Agent run started ~06:22 UTC (01:22 CDT).

## Quota check (pre-submit)

| Source | What it shows |
|--------|----------------|
| `agent/state.json` | Only **2026-09-15 cycle01** recorded as submitted. **0/5** slots for 2026-09-16. |
| GitHub Actions `casmi-loop` log (run 35040180158, ~03:40 UTC) | `competition_submissions` snapshot: **two** rows, both with `publicScore=None` in the API dump: id **56258556** `v0.2 ban-poisoned-exact-dup-IKs + entropy/modcos hybrid + all-libs`; id **56253059** `v0.1 retrieval+symbolic preferred-libs modified-cosine`. |
| Cycle01 committed Analysis | v0.1 public score **0.143** (kernel v2, COMPLETE). Treat that as the last **known** scored result. |
| Sep 15 cycle02 | Docs exist on `main`, but the Actions implement+push of kernel **v4** ended `KERNELWORKERSTATUS.ERROR` after a 18000 s poll. **No cycle02 Kaggle code submit.** |
| Actions run 35060763114 | `in_progress` since 05:45 UTC — still **Sep 15** competition-day slot 2 (started 00:45 CDT, before 01:00). Does **not** consume 2026-09-16 quota unless it somehow submits after the clock rollover *and* Kaggle counts calendar UTC (we still treat Chicago 01:00 as the quota day). |

**Conclusion:** `submissions_today` for Chicago day 2026-09-16 is **0 (&lt; 5)**. Proceed with cycle01. Re-check via Kaggle API immediately before `competition_submit_code` if credentials are available.

Cloud Agent env did **not** inject `KAGGLE_USERNAME` / `KAGGLE_KEY` at process start. GitHub Actions has those secrets (workflow step “Require Action secrets” succeeded). This analysis records that gap; the cycle still prepares a code submit.

## Leaderboard context (public page, 2026-09-16)

| Rank | Team | Public MRR@25 |
|------|------|----------------|
| 1 | GUAM | **0.332** |
| 2 | Minal kharat123 | 0.324 |
| 3 | Ben Pepper | 0.310 |
| 9–10 | Octavi Grau / oz chemicalers | 0.285 |
| — | **our best known** | **0.143** |

Participation on the competition page: ~155 teams, ~510 submissions. Gap vs top is now **~2.3×** (was ~2× when top was 0.285).

## Why score is low (evidence, unchanged physics)

From `Analysis/2026-09-15_cycle01_submission.md` / local `outputs/candidate_evidence.parquet` (v0.1):

1. **Exact test↔train duplicate contamination.** Every molecule had rank-1 `best_similarity = 1.0`, `mass_error_ppm = 0`, library **enveda-180**. Rank-1 SMILES inchikey14 agreed 400/400 with that train label, yet public MRR@25 = **0.143** ⇒ ~86% of duplicated train labels ≠ competition GT.
2. **Cosine saturation.** Aggregation cannot recover when the poisoned hit is perfect.
3. **v0.2 intended fix is unscored.** State marks cycle01 submitted (`v0.2 … + entropy/modcos hybrid + all-libs`) but `public_score` is still null. API dump also returned null. We **must not invent** a v0.2 LB number.
4. **Sep 15 slot 2 never scored.** OpenAI (or fallback-adjacent) applied `MASS_TOL_PPM=15`, `MASS_TOL_PPM_BACKFILL=20` on top of Grok’s unused `ENTROPY_WEIGHT=0.70` spec; kernel v4 ERROR; poller did not treat `KERNELWORKERSTATUS.ERROR` as terminal.

## Concrete improvements for this slot

1. **Major scoring ablation:** `ENTROPY_WEIGHT: 0.55 → 0.70` (the cycle02 bet that never ran). Keep `EXCLUDE_EXACT_DUPLICATES=True`.
2. **Submit-path repair (required, not a second scoring factor):** parse Kaggle `KernelWorkerStatus.ERROR`; pip-install RDKit from the attached wheels dataset when `import rdkit` fails; line-buffer logs.
3. Do **not** also tighten mass windows this slot (that was the failed v4 experiment).
4. Always notebook `competition_submit_code` — never CSV `competitions submit`.

## Naive baselines (local, not LB)

Mass-only known-spectrum CV MRR@25 ≈ 0.73 — only meaningful when labels match GT; not comparable under contamination.
