# Analysis — 2026-09-18 cycle01

## Competition-day quota

- **Clock:** 2026-09-18 01:02 America/Chicago (day start 01:00). This is cycle **01** of Chicago day 2026-09-18.
- **Kaggle API from this Cloud Agent:** `KAGGLE_USERNAME` / `KAGGLE_KEY` are **not** injected into the Cursor Automation environment, so `kaggle competitions submissions` cannot be run here. Quota is inferred from GitHub Actions `casmi-loop` logs (those runners **do** have the secrets).
- **casmi-loop 35311548455** (2026-09-18T05:37Z, still Chicago day 2026-09-17 until 06:00Z):
  - `submissions used today (2026-09-18): local=0 kaggle=0`
  - Listed newest Kaggle rows (public scores still empty):

| id | publicScore | status (at list time) | description |
|----|-------------|------------------------|-------------|
| 56298621 | None | listed | cycle05: broader libs / mass filters / entropy-modcos |
| 56290985 | None | listed | cycle04: mass tolerance optimization |
| 56290242 | None | listed | cycle03: mass tolerance refinement |
| 56289785 | None | listed | 2026-09-16 v10 rdkit-install fix + all-libs entropy/modcos |
| 56289779 | None | listed | probe v3 |

- **Conclusion:** Chicago day 2026-09-18 has **0 / 5** code submits so far. **Not a quota skip.** The 05:37Z Actions job then died on OpenAI HTTP 429 before it could implement or submit.

## Last scored vs leaders

- Best **scored** public MRR@25 we trust: **0.143** (v0.1, kernel v2, 2026-09-15).
- Public leaderboard (Kaggle, ~33% of test): **GUAM 0.332**, then 0.324 / 0.319 / 0.311 / 0.310. Gap is still ~2×.
- Later kernels (v10–v13, submits 56289785–56298621) have **no publicScore in the Actions briefing**. They may still be pending scoring, or they completed the kernel but failed competition scoring. Either way we cannot treat 0.143 as beaten.

## What the last configs actually did

| Cycle | Kernel | Patch (from `agent/state.json`) | Issue |
|-------|--------|----------------------------------|-------|
| 2026-09-15 c01 | v3 | ban exact-dup IKs + entropy hybrid + all libs | intended v0.2; public score unknown |
| 2026-09-17 c03 | v11 | `MASS_TOL_PPM=5`, backfill 10 | tiny window; may starve candidates |
| 2026-09-17 c04 | v12 | ppm 10/15, exclude dups | mass retune, not a new mechanism |
| 2026-09-17 c05 | v13 | entropy 0.6, ppm 10/15, **`TOP_PEAKS=5`**, top cand/spectrum 25 | **peak budget collapsed to 5** |

`casmi26/config.py` on `main` still has `TOP_PEAKS = 5`.

## Why the score is low (evidence)

1. **Poisoned exact duplicates (v0.1, still the ceiling unless we ignore those labels).** Local evidence: every molecule had rank-1 `best_similarity=1.0` from `enveda-180` clones whose train SMILES ≠ competition GT → public 0.143. Exclude-exact-dups remains mandatory.
2. **`TOP_PEAKS=5` is a retrieval self-own.** Li & Fiehn / Flash Entropy keep all ions above 1% BPI (`max_peak_num` unlimited or 1000). Five peaks:
   - Destroy entropy similarity (the metric is defined on the full cleaned spectrum).
   - Make modified cosine compare 5-ion cartoons.
   - Make `spectra_identical()` compare 5-peak fingerprints, so **non-identical** spectra can be banned as “poisoned IKs.”
3. **Mass-ppm churn without peak fidelity.** Cycles 03–04 only moved ppm. That cannot recover signal that was never in the cleaned vectors.
4. **Unscored later submits.** Until Kaggle returns a publicScore, we must not assume entropy/all-libs already worked.
5. **Actions reliability.** OpenAI 429 aborted the first 2026-09-18 slot. The loop should fall back to deterministic ablations instead of exiting 1.

## Concrete improvements for this slot

- **One major factor:** restore `TOP_PEAKS` **5 → 128** (original v0.2 spec; still conservative vs msentropy).
- Keep `EXCLUDE_EXACT_DUPLICATES=true`, `ENTROPY_WEIGHT=0.6`, mass 10/15 ppm unchanged so the slot is a clean peak-count ablation.
- Rebuild the internet-off kernel and submit via `competition_submit_code` (never CSV).
- Harden `scripts/casmi_loop/chatgpt_spec.py` so HTTP 429/5xx uses `FALLBACK_ABLATIONS` instead of crashing the hourly runner.

## Cloud-agent constraint / submit outcome

This runner can write docs/code/PR. GitHub Actions has Kaggle secrets; this Cursor Automation currently does **not** (`KAGGLE_USERNAME`, `KAGGLE_KEY`, `KAGGLE_API_TOKEN` all unset; `~/.kaggle/` empty). `kaggle kernels push` and `KaggleApi.authenticate()` both fail with “Authentication required” (kaggle CLI 2.2.4). **No code submission was created from this cycle.** Quota is not exhausted; the skip is missing Cloud secrets, not the 5-slot cap.

`casmi-loop` on GitHub can still submit this ablation after merge: `write_cycle_docs` reuses these substantial Research/Analysis/Hypothesis files and applies the spec `config_patch`.
