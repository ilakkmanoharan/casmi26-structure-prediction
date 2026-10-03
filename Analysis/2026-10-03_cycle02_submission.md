# Analysis — 2026-10-03 cycle02

## Quota (re-checked 2026-10-03T06:05Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago**. Now = 01:05 CDT.

| Clock | Used | Limit | Notes |
|-------|------|-------|-------|
| **Chicago 01:00** (CLOUD_CYCLE_PROMPT) | **0/5** | 5 | No submit since 2026-10-03 01:00 CDT (06:00 UTC) |
| **UTC calendar** (Kaggle reset + Actions `competition_day()`) | **1/5** | 5 | Actions [37081255626](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/37081255626) → Kaggle **56785817** kernel v49 `2026-10-03_cycle01 H-top-peaks` at 00:43Z (**before** 01:00 CDT) |

**Decision:** proceed with `2026-10-03_cycle02`. Not quota-exhausted.

Cursor Cloud env still has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (Python `os.environ` empty; `kaggle` 2.2.4 → 401). Wrote `~/.kaggle/kaggle.json` mode 0600 from empty values — unusable. Live list/leaderboard via CLI failed. Counts above come from `agent/state.json` + `gh run` + last Actions analysis dump.

## Recent submissions (from `agent/state.json` + Actions cycle01 dump)

Newest first; publicScore from Kaggle API is consistently `None` even when status is COMPLETE.

| Kaggle id | Kernel | Message | When (UTC) | Public |
|-----------|--------|---------|------------|--------|
| 56785817 | v49 | 2026-10-03_cycle01 H-top-peaks | 00:43 10-03 | None (COMPLETE) |
| 56782190 | v48 | 2026-10-02_cycle04 H-peaks | 20:53 10-02 | None |
| 56777422 | v47 | 2026-10-02_cycle03 H-mass-wide | 15:56 10-02 | None |
| 56769746 | v46 | 2026-10-02_cycle02 H-entropy | 08:29 10-02 | None |
| 56763204 | v45 | 2026-10-02_cycle01 H-top-peaks | 01:41 10-02 | None |
| 56759705 | v44 | 2026-10-01_cycle03 H-mass-wide | 22:02 10-01 | None |

Best **scored** public we still trust: **0.143** (v0.1 exact-dup / poisoned `enveda-180` labels).

## Why score is low

1. **Poisoned exact duplicates.** v0.1 matched identical test↔train spectra whose train InChIKey ≠ GT. That single failure mode caps public MRR near 0.143 even with a “perfect” library hit. Guard is on (`EXCLUDE_EXACT_DUPLICATES=True`) but we still need *non-identical* evidence to rank the true structure.
2. **Fallback carousel is saturated.** Actions slots 1–4 re-apply constants already live on `main` (128 peaks, entropy 0.75, mass 35/80, min-sim 0.05). Those submits COMPLETE but cannot move the metric.
3. **Cleaning is one decade too loose vs the entropy papers.** `INTENSITY_FLOOR=0.001` keeps 0.1% ions. After TOP_PEAKS=128, those ions occupy match slots in greedy alignment and pull entropy/modcos toward noisy library spectra (including remaining near-dups).
4. **Leaderboard gap is analog / multi-channel, not ppm.** CLIST prize table 2026-10-03: **pikachu 0.47**, chopper/Randy **0.44**, Ozymandias31415 **0.43**. Public notebooks: analog / four-channel rankers **0.328–0.339**. Retrieval-only config tweaks will not close 0.143→0.47; they can still stop wasting tickets and reduce noise-driven rank errors.

## Concrete improvement for this slot

One major factor vs live `main`: **`INTENSITY_FLOOR` 0.001 → 0.01** (Flash / msentropy `noise_threshold`).

Also retarget Actions **slot-2** fallback `H-entropy` → `H-intensity` so the next hourly `casmi-loop` (secrets live there) does not burn ticket 2 on a no-op `ENTROPY_WEIGHT=0.75`.

Cloud PRs #13–#16 already proposed this ablation and stayed draft/unmerged. Merge this PR before the next Actions hour or slot 2 wastes another ticket.

## Cycle outcome

Implemented `INTENSITY_FLOOR=0.01`, rebuilt kernel (`enable_internet: false`), pytest **23 passed**. **Did not** `kernels push` / `competition_submit_code`: Cloud env still lacks Kaggle secrets (401). Actions slot-2 fallback retargeted to H-intensity so the next hourly `casmi-loop` can submit this ticket if this PR is on `main`.

## Out of this write-up

No claim that retrieval solves Class-3 de novo. No CSV submit.
