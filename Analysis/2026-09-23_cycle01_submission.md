# Analysis — 2026-09-23 cycle01

## Quota (do not skip)

Chicago competition day **2026-09-23** opened at 01:00 America/Chicago (06:00 UTC). This Cloud Automation fired at 06:00 UTC.

GitHub Actions `casmi-loop` run **35823205794** (2026-09-23 05:37Z, scheduled) printed:

```
submissions used today (2026-09-23): local=0 kaggle=0
=== casmi-loop 2026-09-23 slot 1 ===
```

then died on `urllib.error.HTTPError: HTTP Error 429: Too Many Requests` inside `_openai_json` **before** implement or submit. **Not a quota skip.** Used slots: **0/5**.

This Cloud Agent still has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` in the environment (`~/.kaggle` is empty). `write_kaggle_credentials()` returned False; no `kaggle.json` was written. Cannot call the Kaggle CLI here. Quota evidence is the Actions API listing (trusted: same repo, Actions has the secrets).

## Recent Kaggle submissions (from Actions 35823205794 briefing)

Newest first; public scores still **null**:

| id | publicScore | description |
|----|-------------|-------------|
| 56298621 | None | cycle05: broader libs + entropy/modcos + **TOP_PEAKS=5** (kernel v13) |
| 56290985 | None | cycle04 mass-tol optimization (v12) |
| 56290242 | None | cycle03 mass-tol refinement (v11) |
| 56289785 | None | 2026-09-16 v10 rdkit-install fix + all-libs entropy/modcos |
| 56289779 | None | probe v3 |

Last **successful** Actions submit remains **35194073264 → 56298621** (2026-09-17). Every hourly run since 2026-09-18 05:37Z has failed on OpenAI HTTP 429 (35311548455, 35421305696, 35492737629, 35561902203, 35685129013, **35823205794**). Draft PRs #4–#8 already restore `TOP_PEAKS=128` but are unmerged; **main still has `TOP_PEAKS=5`**.

## Why the score is low

1. **v0.1 (~0.143)** trusted exact test↔train spectrum duplicates in `enveda-180` whose train InChIKeys ≠ competition GT. Rank-1 similarity = 1.0 everywhere; MRR collapses.
2. **v0.2+** banned those IKs and switched to entropy/modcos + all libs, but later slots **never scored** (null publicScore).
3. **cycle05 / 56298621** then set `TOP_PEAKS=5`. Entropy similarity (Li & Fiehn) is designed to keep low-abundance fragment ions; a 5-peak view throws the ladder away and makes the hybrid almost a 5-ion cosine. `clean_spectrum` default is 64; cycle02 spec was 128; Flash Entropy default is “all ions above ~1% BPI”.
4. Public LB (Kaggle page + CLIST snapshot 2026-09-23): **GUAM 0.332**. Our best *scored* public is still **0.143**. A 09-22 cloud note recorded Ozymandias31415 at 0.415; today’s public table lists that team at 0.298 — treat 0.332 as the current top.

## Concrete improvement for this slot

Restore **`TOP_PEAKS=128`** as the single major ablation vs the last submitted kernel. Also make `_openai_json` return `None` on HTTP 429/URL errors so the next hourly `casmi-loop` uses deterministic fallback / pre-written docs instead of crashing with quota remaining.

Do **not** also retune mass tolerance or entropy weight in this slot.

## Cloud submit status

`kaggle kernels push` / `competition_submit_code` cannot run from this agent until Cursor Automation secrets `KAGGLE_USERNAME` and `KAGGLE_KEY` (and `KAGGLE_API_TOKEN` for CLI 2.2) are injected. After this PR merges, hourly Actions can reuse these substantial docs (`_substantial` ≥400 chars) and submit **without** calling OpenAI.
