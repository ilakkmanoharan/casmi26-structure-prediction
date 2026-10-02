# Analysis — 2026-10-02 cycle02

## Clock and quota

- Trigger: Cloud Automation cron `0 6 * * *` at **2026-10-02T06:04:05Z** = **01:04 CDT** (first Chicago slot).
- Competition day start: **01:00 America/Chicago**.
- **Chicago-clock submits since 01:00 CDT: 0/5.**
- **Kaggle UTC-day 2026-10-02: 1/5** (Actions burned slot 1 before Chicago midnight+1h).
- Quota is **not** exhausted. Cloud cannot confirm via API: `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are absent in this environment (same failure as 09-25/09-26/10-01 Cloud runs). Counts below come from `agent/state.json` + `gh run list`.

## Recent submissions (from committed state + Actions)

| When (UTC) | Runner | Kaggle id | Kernel | Message | Public score |
|------------|--------|-----------|--------|---------|--------------|
| 2026-10-02 01:41 | github_actions 36950737961 | 56763204 | v45 | 2026-10-02_cycle01 H-top-peaks | null |
| 2026-10-01 22:02 | github_actions | 56759705 | v44 | 2026-10-01_cycle03 H-mass-wide | null |
| 2026-10-01 16:25 | github_actions | 56754985 | v43 | 2026-10-01_cycle02 H-entropy | null |
| 2026-10-01 08:56 | github_actions | 56747915 | v42 | 2026-10-01_cycle01 H-top-peaks | null |
| 2026-09-30 23:16 | github_actions | 56721177 | v40 | 2026-09-30_cycle05 H-domain | null |

Best *scored* public in `agent/state.json`: **0.143** (v0.1). Later submits stay `public_score: null` — Kaggle often delays notebook-competition scoring.

No `casmi-loop` run is in progress. Last scheduled success: 36950737961 (17m30s, 01:23Z).

## Why the score is low

1. **Poisoned exact duplicates (v0.1).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey/SMILES ≠ competition GT. Perfect library match still scores ~0.143. `EXCLUDE_EXACT_DUPLICATES=True` is on; we must keep ranking from *non-identical* evidence.
2. **Cleaning mismatch with entropy literature.** Live main uses `INTENSITY_FLOOR=0.001` (0.1% of base peak). Li/Fiehn Flash Entropy and `ms-entropy` drop ions **<1% of max**. The extra 10× noise ions inflate spectral entropy, flatten `_entropy_weights`, and create spurious modified-cosine peak pairs — exactly the failure mode that keeps decoys in the top-25 after the exact-dup ban.
3. **Fallback rotation is exhausted as a source of *new* signal.** Slot 1 `TOP_PEAKS=128` and slot 2 `ENTROPY_WEIGHT=0.75` are already the live constants. Today’s UTC slot 1 was a no-op ticket. Slot 2 as currently coded would be another no-op.
4. **Leaderboard gap.** Public top **GUAM 0.332** (Kaggle prize-contender table, 2026-10-02). Analog/quad-channel community kernels 0.33–0.339. Our 0.143 is retrieval-without-analogue plus the poisoned-label leak. Retrieval alone does not solve Class-3.

## What to change this slot

**One major factor:** `INTENSITY_FLOOR` 0.001 → **0.01**.

Do **not** re-submit H-entropy / H-top-peaks / H-mass-wide. Those have been the last ~10 tickets with no scored movement.

If Cloud still cannot `kernels push`, land the patch + retarget Actions **slot 2** fallback to `H-intensity` so the next hourly `casmi-loop` spends UTC ticket 2 on this ablation instead of rewriting `ENTROPY_WEIGHT=0.75`.

## Held evidence

- Live `casmi26/config.py` after 10-02 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `MASS_TOL_PPM=35`, `MASS_TOL_PPM_BACKFILL=80`, `TOP_K_SPECTRA_PER_QUERY=120`, `MIN_SIMILARITY=0.05`, `INTENSITY_FLOOR=0.001`, `PEAK_MZ_TOL=0.01`, `EXCLUDE_EXACT_DUPLICATES=True`.
- Draft Cloud PRs #13/#14/#15 already argued this floor; none merged, so Actions never submitted it.
