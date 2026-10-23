# Analysis — 2026-10-23 cycle02

## Quota (checked 2026-10-23T06:02Z)

- **Competition clock:** day starts 01:00 America/Chicago. Wall clock at trigger: **01:01 CDT**. Chicago-day **2026-10-23** just opened.
- **Chicago-clock submits since 01:00 CDT:** **0/5**. Proceed.
- **UTC-calendar quota (Kaggle midnight reset, Actions `competition_day()`):** **1/5**.
- Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so the live Kaggle submissions API could not be queried from this pod. Count below is from `agent/state.json` + `gh run list`.

## Recent submissions (from `agent/state.json`, newest first)

| When (UTC) | Kaggle id | Kernel | Message | Public score |
|------------|-----------|--------|---------|--------------|
| 2026-10-23T04:16Z (Actions 39897609691) | **57548841** | v139 | 2026-10-23_cycle01 H-top-peaks | null |
| 2026-10-22T23:19Z | **57540687** | v138 | 2026-10-22_cycle05 H-domain | null |
| 2026-10-22T19:25Z | **57536123** | v137 | 2026-10-22_cycle04 H-peaks | null |
| 2026-10-22T15:14Z | **57529516** | v136 | 2026-10-22_cycle03 H-intensity | null |
| 2026-10-22T09:33Z | **57519024** | v135 | 2026-10-22_cycle02 H-entropy | null |
| 2026-10-22T04:08Z | **57508910** | v134 | 2026-10-22_cycle01 H-top-peaks | null |

Every scored public result we still have is **0.143** (v0.1). Later code submits stay `null` on the public board — Kaggle often delays or withholds notebook scores, so we cannot treat “null” as a lift.

UTC ticket 1 today (`TOP_PEAKS=128`) did **not** change live main. Live constants after that submit:

| Constant | Live main |
|----------|-----------|
| `MASS_TOL_PPM` / backfill | 35.0 / 80.0 |
| `PEAK_MZ_TOL` | **0.01** |
| `TOP_PEAKS` | 128 |
| `INTENSITY_FLOOR` | 0.01 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `ENTROPY_WEIGHT` | 0.75 |
| `EXCLUDE_EXACT_DUPLICATES` | true |

## Why the score is still low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies in `enveda-180` carry train InChIKey14s that do **not** match competition GT. Perfect library match → wrong rank-1. Exclusion is on; that alone cannot create a correct structure when the true molecule is absent or only present as a CE-shifted analog.
2. **Fragment pairing is tighter than the literature default.** `hybrid_similarity` / modified cosine use `tol=cfg.peak_mz_tol` (10 mDa). Flash Entropy, ms_entropy, and matchms default to **20 mDa**. GNPS / MassBank / MONA / Enveda spectra are not centroided to the same grid; a 10 mDa cut drops true fragment pairs after CE or instrument shift, so the correct InChIKey14 never clears `MIN_SIMILARITY=0.05`.
3. **Slot rotation has been a no-op for weeks.** Actions fallbacks 1–3 (`TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`) are already live. Replaying H-entropy on UTC ticket 2 would not change the spectrum or the score object.
4. **Leaderboard gap.** CLIST (~16h stale at 06:00Z): **Oleksandr Parfionov 0.50**, **pikachu 0.50**, **CHU1PC 0.50**, Savko 0.49, MarvinTMB / Oliver Ford / Dunyuan Zha / Parth Talsania 0.48. Community analog notebooks ~0.43–0.46. We are an order of magnitude below the public frontier; retrieval-only will not close that gap if the true structure is missing, but a 20 mDa window is the cheapest unused fix that can recover CE-shifted true hits.

## Concrete improvement this slot

Implement **one** major ablation: `PEAK_MZ_TOL` **0.01 → 0.02**.

Retarget Actions **slot-2** fallback from H-entropy (already live) to H-peak-mz so the next unused casmi-loop hour (~09:00 UTC historically; hourly cron is delayed) does not waste UTC ticket 2 on `ENTROPY_WEIGHT=0.75`.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on a no-op unless it reuses these cycle02 docs from main (`_substantial` ≥ 400 chars + `config_patch: {"PEAK_MZ_TOL": 0.02}`).
