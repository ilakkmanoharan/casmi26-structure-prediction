# Analysis — 2026-10-28 cycle02

## Quota (checked 2026-10-28T06:02Z)

| Clock | Used / 5 | Notes |
|-------|----------|-------|
| **Kaggle / Actions UTC calendar** | **1 / 5** | Actions `casmi-loop` run 40634007274 (scheduled 04:44Z, ~18m) → Kaggle **57724850**, kernel v163, `2026-10-28_cycle01 H-top-peaks`. Next unused UTC ticket is **2**. |
| **CLOUD_CYCLE_PROMPT Chicago 01:00** | **0 / 5** | Day opened 01:00 CDT = 06:00 UTC. The 05:02Z submit was 00:02 CDT (still Chicago day 10-27). |

**Not exhausted.** Do not exit. Cloud cannot call `kaggle competitions submissions` this run: `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are **absent** from the Cursor Cloud environment (confirmed `env | grep -i kaggle` empty; `~/.kaggle/` exists but has no `kaggle.json`). Submission count below is from `agent/state.json` + `gh run list`, not a live Kaggle API dump.

## Recent public scores + messages

Best scored public still **0.143** (v0.1). Later code submits complete with `publicScore=None` in state — Kaggle has not published a higher scored row for this kernel.

From `agent/state.json` (newest first):

| Kaggle id | Kernel | When (UTC) | Message | Patch | Public |
|-----------|--------|------------|---------|-------|--------|
| 57724850 | v163 | 2026-10-28 05:02 | cycle01 H-top-peaks | `TOP_PEAKS=128` | null |
| 57716036 | v162 | 2026-10-27 23:56 | cycle05 H-domain | `{}` | null |
| 57712244 | v161 | 2026-10-27 20:12 | cycle04 H-peaks | `TOP_PEAKS=160`, `MIN_SIMILARITY=0.05` | null |
| 57704012 | v160 | 2026-10-27 14:27 | cycle03 H-peak-mz | `PEAK_MZ_TOL=0.02` | null |
| 57693774 | v159 | 2026-10-27 07:46 | cycle02 H-peak-mz | `PEAK_MZ_TOL=0.02` | null |
| 57685058 | v158 | 2026-10-27 01:34 | cycle01 H-top-peaks | `TOP_PEAKS=128` | null |

Actions 10-27 cycle02/03 **replayed already-live** `PEAK_MZ_TOL=0.02` because Cloud PR **#39** (H-min-sim) was not merged before the hourly cron. Same failure mode as 10-26 (PR #38).

## Leaderboard context (CLIST, updated ~2026-10-28T01:00Z)

[CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) (rounded):

- **Savko 0.51**, **Parfionov 0.51**
- pikachu / Shehab / CHU1PC **0.50**
- Cluster at 0.48–0.49 through rank ~20
- Community analog notebooks historically ~0.43–0.46

Gap from our 0.143 to the 0.50 frontier is not a 10 mDa pairing miss (already live) and not a 128-peak ladder miss (already live). Top teams use analog propagation / extra evidence channels. Our next *retrieval* lever that is still unused is the **admission floor**.

## Why score is low

1. **v0.1 exact-dup poison (still the scored 0.143 row).** Exact test↔train spectrum duplicates in `enveda-180` carry train labels that do **not** match competition GT. `EXCLUDE_EXACT_DUPLICATES=True` stays on; retrieval still cannot invent the true Class-3 structure when the library row is wrong.

2. **`MIN_SIMILARITY=0.05` admits junk into MRR@25.** `casmi26/retrieve.py` keeps every `hybrid_similarity >= cfg.min_similarity`. Li/Fiehn 2021 want entropy similarity **> 0.75** for FDR < 10%. MS2Query operators discard model scores below ~0.6. At 0.05, `top_k=120` and the 25-slot SMILES list fill with near-random library hits, so a mid-score true InChIKey14 is pushed past rank 25 (MRR contribution 0).

3. **Slot rotation has been a no-op for days.** Live main after Actions 10-28 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-2 fallback on main) does not change the spectrum object.

## Concrete improvements for the next slot

- **This slot (cycle02):** `MIN_SIMILARITY` 0.05 → **0.12**. One major factor. Hold all other constants.
- **Retarget Actions fallbacks** so 07:00 UTC cron cannot waste ticket 2 on `PEAK_MZ_TOL=0.02`: slot-2 → H-min-sim; slot-3 → H-peaks (`TOP_PEAKS=160` only, do not reset `MIN_SIMILARITY`).
- **Do not dispatch** `casmi-loop` from this unmerged branch (would submit live main = already-live pairing).
- Next unused after this merges: `TOP_PEAKS` 128 → 160 (slot-3), then a higher floor (0.20) or analog channel — not another 0.02 Da replay.

## Cloud submit status

`write_kaggle_credentials()` returns false without env secrets. No `kernels push`, no `competition_submit_code`. Record `skipped_reason=cloud_missing_kaggle_secrets`. Merge before the next unused casmi-loop hour (~07:00 UTC) or UTC ticket 2 is wasted on H-peak-mz again.
