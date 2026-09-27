# Analysis — 2026-09-27 cycle02

## Clock and quota

- **Cloud run:** 2026-09-27T06:00Z cron (`0 6 * * *`). Chicago wall clock **01:01 CDT** — first slot after competition-day start **01:00 America/Chicago**.
- **Kaggle secrets in this Cloud environment:** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent**. `~/.kaggle/` exists but is empty; `kaggle`  CLI returns "Authentication required". Could not write `kaggle.json` or call `kaggle competitions submissions`. Quota below is reconstructed from GitHub Actions + committed `agent/state.json` + the public leaderboard (no secret values).
- **UTC / Kaggle reset day 2026-09-27:** Actions run [36284718595](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/36284718595) at 01:10Z submitted **56594353** (`2026-09-27_cycle01 H-top-peaks`, kernel v23). Local state has that one submitted slot. **Kaggle UTC quota is 1/5**, not exhausted.
- **Chicago competition day 2026-09-27** (started 06:00Z / 01:00 CDT): the Actions submit landed at 01:33Z on **Chicago day 2026-09-26**. Chicago-clock submits since 01:00 CDT today: **0/5**.
- **Decision:** do **not** exit for quota. Cycle tag = next unused `2026-09-27_cycle02`.

## Recent public scores + messages

From `agent/state.json` plus Actions 36284718595 (newest first):

| id | publicScore | status | description |
|----|-------------|--------|-------------|
| 56594353 | null | COMPLETE | 2026-09-27_cycle01 H-top-peaks · kernel v23 · `TOP_PEAKS=128` |
| 56587793 | null | COMPLETE | 2026-09-26_cycle05 H-domain |
| 56585104 | null | COMPLETE | 2026-09-26_cycle04 H-peaks · `TOP_PEAKS=160`, `MIN_SIMILARITY=0.05` |
| 56580060 | null | COMPLETE | 2026-09-26_cycle03 H-mass-wide |
| 56573187 | null | COMPLETE | 2026-09-26_cycle02 grok-docs · `ENTROPY_WEIGHT=0.75` |
| 56565919 | null | COMPLETE | 2026-09-26_cycle01 H-top-peaks |
| 56561301 | null | COMPLETE | 2026-09-25_cycle04 H-peaks |
| 56557839 | null | COMPLETE | 2026-09-25_cycle03 H-mass-wide |
| 56551985 | null | COMPLETE | 2026-09-25_cycle02 H-mass-tight |
| 56544614 | null | COMPLETE | 2026-09-25_cycle01 grok-docs |

**Best scored public still 0.143 (v0.1).** Later code submits have not published a publicScore in the API snapshots recorded in Analysis/. Live public LB (fetched 2026-09-27T06:05Z): **#1 Ozymandias31415 0.425**; #2 pikachu 0.421; #3 Udam Liyanage 0.412. Gap vs our last scored run ≈ **0.28**.

## Why the score is low

1. **Poisoned exact duplicates (unchanged).** Exact test↔train spectra in `enveda-180` carry train labels that are **not** competition GT. A perfect cosine/entropy match on those rows ranks the wrong SMILES #1 and caps MRR. Ban is on; we must rank from *non-identical* evidence.
2. **Weak neighbors fill the top-25.** After the ban, `retrieve_for_spectrum` still accepts hybrid scores ≥ **0.05**. That is far below Li et al. 2021's FDR<10% identity point (entropy 0.75). Mass-window decoys with a few shared fragments occupy ranks that should stay empty or go to stronger analogues. MRR@25 only rewards the first correct structure; decoys above it are lethal.
3. **Yesterday's entropy-dominant mix is already on main.** `ENTROPY_WEIGHT=0.75` landed in 2026-09-26_cycle02 / kernel v19. Repeating H-entropy (current Actions slot-2 fallback) is a no-op.
4. **Mass / peaks / domain already swept (09-25 and 09-26).** Tight 15/40, wide 35/80, peaks 160, domain-prior boost — all publicScore still null. Repeating them is not an information gain.
5. **Retrieval cannot solve Class-3.** Public 0.33–0.42 notebooks advertise analogue / multi-channel rankers. Our kernel is still exact-mass library search. A higher similarity floor is the largest *unused* in-kernel lever among existing constants.

## Concrete improvement for this slot

- **One major factor:** `MIN_SIMILARITY`: 0.05 → **0.12**.
- Hold: `TOP_PEAKS=128`, `MASS_TOL_PPM=35`, `MASS_TOL_PPM_BACKFILL=80`, `TOP_K_SPECTRA_PER_QUERY=120`, `ENTROPY_WEIGHT=0.75`, `EXCLUDE_EXACT_DUPLICATES=True`.
- Retarget Actions fallback slot 2 from no-op `H-entropy` to this same `H-min-sim` patch so the next `casmi-loop` run does not waste UTC slot 2.
- Submit path: `kaggle kernels push` + `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **This Cloud run cannot push/submit** until Kaggle secrets are attached to the automation. Docs + config are written so the next `casmi-loop` slot reuses them.

## Cloud submit blocker

Same as 2026-09-25 / 2026-09-26 Cloud cycles: environment install does not inject `KAGGLE_USERNAME` / `KAGGLE_KEY`. Analysis of quota used Actions + public LB only. If a later runner has secrets, it should submit this cycle's kernel rather than inventing a second ablation.
