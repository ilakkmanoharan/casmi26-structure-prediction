# Analysis 2026-09-25_cycle01 — why MRR is low and what to change

Competition day: **2026-09-25** (anchor 01:00 America/Chicago).  
Triggered at 06:04 UTC (01:04 CDT). Cycle **01** of 5.

## Quota check (do not submit if 5 already used)

Cloud Agent env still has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (same as 2026-09-18…09-24 cloud cycles). Direct `kaggle competitions submissions` could not be run from this pod.

Quota inferred from GitHub Actions `casmi-loop` run **36081142271** (2026-09-25T01:14:27Z, **failure** on OpenAI HTTP 429 *before* any submit):

```
submissions used today (2026-09-25): local=0 kaggle=0
=== casmi-loop 2026-09-25 slot 1 ===
kaggle submissions [
  (56298621, None, '…broader candidate libraries…'),
  (56290985, None, 'Optimizing mass tolerance…'),
  (56290242, None, 'Refining mass tolerance…'),
  (56289785, None, '2026-09-16 v10 rdkit-install fix + all-libs entropy/modcos'),
  (56289779, None, 'probe v3')
]
```

- **Used today (Chicago 01:00 day): 0 / 5.** Quota is **not** exhausted.
- Actions’ `competition_day()` is UTC calendar date; this cloud prompt uses Chicago 01:00. Both clocks agree it is 2026-09-25 and kaggle count is 0.
- Hourly Actions has failed every run since 2026-09-18 05:37Z on OpenAI **429** in `_openai_json` (no fallback). Last successful code submit: **56298621** (2026-09-17 cycle05, kernel v13).
- Public scores on those five newest rows are still **null** in the Actions log.

## Public leaderboard context (fetched 2026-09-25)

Live public LB (≈33% of test):

| Rank | Team | Public MRR@25 |
|------|------|----------------|
| 1 | Ozymandias31415 | **0.425** |
| 2 | Udam Liyanage | 0.412 |
| 3 | pikachu | 0.394 |
| 8 | Ozymandias listed 0.298 on 09-24 — **stale**; current top is 0.425 | — |
| — | Our last **scored** public | **0.143** (v0.1) |

Gap to #1: **0.282**. Memory of “GUAM 0.332” from 2026-09-24 is outdated — the board has moved.

Public Code tab notebooks (“analog ranker”, “quad-channel evidence ranker”, “two ranker”) report ~0.32–0.34, consistent with analogue / multi-evidence ranking rather than 5-peak cosine.

## Why our score is low (evidence)

1. **Poisoned exact duplicates (v0.1).** Exact test↔train spectrum copies in `enveda-180` have train labels ≠ competition GT. Perfect library match of those rows yields ~0.143 public. `EXCLUDE_EXACT_DUPLICATES=True` is on and must stay on.

2. **`TOP_PEAKS=5` on `main` (cycle05).** Cycle05 set `TOP_PEAKS=5`. That throws away the fragment ladder entropy similarity was built on (Li et al. 2021; MSEntropy keeps 100–1000 peaks after a 1% noise cut). Cloud cycles 09-18…09-24 all specified restore **128** and opened draft PRs; **none merged**. `main` is still at 5.

3. **Unscored later submits.** 56290242 / 56290985 / 56298621 never produced a public number in Actions logs. We cannot treat mass-tolerance tweaks as validated.

4. **Runner failure, not quota.** Actions dies on OpenAI 429 before `kernels push`. Cloud cannot authenticate to Kaggle. So the 5-slot day is burning on process failures, not experiments.

## Concrete improvements for this slot

1. **Major ablation:** `TOP_PEAKS` 5 → **128**. One factor vs cycle05/`main`.
2. **Unblock Actions:** catch OpenAI HTTP 429/5xx in `_openai_json` and use slot-1 fallback `{TOP_PEAKS: 128}` so the next `casmi-loop` hour can submit if this branch reaches `main`.
3. **Credentials helper:** write `~/.kaggle/kaggle.json` (mode 0600) + `access_token` when env is present (kaggle 2.2.x wants `KAGGLE_API_TOKEN`).
4. **Do not** CSV-submit. **Do not** change entropy weight, mass windows, or domain priors in the same slot.

If this Cloud run still cannot `kernels push`, the code + docs must land on git so Actions (which *has* Kaggle secrets) can submit after the 429 fix.
