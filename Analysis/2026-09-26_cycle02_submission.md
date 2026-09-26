# Analysis — 2026-09-26 cycle02

## Clock and quota

- **Cloud run:** 2026-09-26T06:15Z cron (`0 6 * * *`). Chicago wall clock **01:16 CDT** — first slot after competition-day start **01:00 America/Chicago**.
- **Kaggle secrets in this Cloud environment:** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent**. Could not write `~/.kaggle/kaggle.json` or call `kaggle competitions submissions`. Quota below is reconstructed from GitHub Actions logs + committed `agent/state.json` + the public leaderboard (no secret values).
- **UTC / Kaggle reset day 2026-09-26:** Actions run [36207887386](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/36207887386) at 01:16Z printed `submissions used today (2026-09-26): local=0 kaggle=0`, then `competition_submit_code` → **56565919**. So **Kaggle UTC quota is 1/5**, not exhausted.
- **Chicago competition day 2026-09-26** (started 06:00Z / 01:00 CDT): that Actions submit landed at 01:33Z on **Chicago day 2026-09-25**. Chicago-clock submits since 01:00 CDT today: **0/5**.
- **Decision:** do **not** exit for quota. Cycle tag = next unused `2026-09-26_cycle02`.

## Recent public scores + messages

From Actions 36207887386 (newest first at 01:33Z) plus `agent/state.json`:

| id | publicScore | status | description |
|----|-------------|--------|-------------|
| 56565919 | null | PENDING→COMPLETE (Actions) | 2026-09-26_cycle01 H-top-peaks · kernel v18 · `TOP_PEAKS=128` |
| 56561301 | null | COMPLETE | 2026-09-25_cycle04 H-peaks · `TOP_PEAKS=160`, `MIN_SIMILARITY=0.05` |
| 56557839 | null | COMPLETE | 2026-09-25_cycle03 H-mass-wide · `MASS_TOL_PPM=35`, backfill 80, `TOP_K=120` |
| 56551985 | null | COMPLETE | 2026-09-25_cycle02 H-mass-tight · 15 / 40 ppm |
| 56544614 | null | COMPLETE | 2026-09-25_cycle01 grok-docs · `TOP_PEAKS=128` |
| 56298621 | null | COMPLETE | 2026-09-17 cycle05 broader libs + entropy/modcos 0.6 + `TOP_PEAKS=5` (destructive) |
| 56290985 | null | COMPLETE | mass-tol optimization |
| 56290242 | null | COMPLETE | mass-tol refinement |
| 56258556 | null | COMPLETE | v0.2 ban-poisoned-exact-dup-IKs + hybrid + all-libs |

**Best scored public still 0.143 (v0.1).** Later code submits have not published a publicScore in the API snapshot Actions printed. Live public LB (fetched 2026-09-26T06:16Z): **#1 Ozymandias31415 0.425**; #2 Udam Liyanage 0.412; #3 Naoism 0.401. Gap vs our last scored run ≈ **0.28**.

## Why the score is low

1. **Poisoned exact duplicates (unchanged).** Exact test↔train spectra in `enveda-180` carry train labels that are **not** competition GT. A perfect cosine/entropy match on those rows ranks the wrong SMILES #1 and caps MRR. Ban is on; we must rank from *non-identical* evidence.
2. **Hybrid still cosine-heavy.** `ENTROPY_WEIGHT=0.6` leaves 40% modified-cosine. Cosine saturates on shared fragments and on the leaked identical rows. Li et al. 2021's NP FDR curve uses entropy similarity **0.75** as the <10% FDR operating point — we have never submitted that mix.
3. **`TOP_PEAKS=5` scar (09-17 cycle05) then restore.** Cycle01 today only restored the 128-peak ladder (already the value on main). That is not a new ranking signal.
4. **Mass-window sweep already done (09-25 cycles 2–3).** Tight 15/40 and wide 35/80 did not produce a public score. Repeating them is not an information gain.
5. **Retrieval cannot solve Class-3.** Public 0.33–0.42 notebooks advertise analogue / multi-channel rankers. Our kernel is still exact-mass library search. Entropy-dominant ranking is the largest *in-kernel* lever left among existing constants.

## Concrete improvement for this slot

- **One major factor:** `ENTROPY_WEIGHT`: 0.6 → **0.75**.
- Hold: `TOP_PEAKS=128`, `MASS_TOL_PPM=35`, `MASS_TOL_PPM_BACKFILL=80`, `TOP_K_SPECTRA_PER_QUERY=120`, `MIN_SIMILARITY=0.05`, `EXCLUDE_EXACT_DUPLICATES=True`.
- Submit path: `kaggle kernels push` + `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **This Cloud run cannot push/submit** until Kaggle secrets are attached to the automation. Docs + config are written so the next `casmi-loop` slot reuses them.

## Cloud submit blocker

Same as 2026-09-25 Cloud cycle01: environment install does not inject `KAGGLE_USERNAME` / `KAGGLE_KEY`. Analysis of quota used Actions + public LB only. If a later runner has secrets, it should submit this cycle's kernel rather than inventing a second ablation.
