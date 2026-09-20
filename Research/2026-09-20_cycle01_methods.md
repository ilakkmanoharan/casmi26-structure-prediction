# Research 2026-09-20_cycle01 — fragment-ladder retrieval for MRR@25

Chicago competition day 2026-09-20 (01:00 America/Chicago). Notebook-only kernel,
internet off. Goal: raise public MRR@25 from **0.143** toward the live public
leaderboard top (**GUAM 0.332**; next 0.324 / 0.319 as of this cycle).

## Sources reviewed

| Source | Why it matters |
| --- | --- |
| Li et al., *Nat Methods* 2021 — [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) | Entropy similarity beat 42 scores on NIST20; low-abundance ions carry isomer signal; FDR <10% at entropy 0.75 on natural-product spectra. |
| Li & Fiehn, *Nat Methods* 2023 — [Flash entropy search](https://doi.org/10.1038/s41592-023-02012-9) | Identity / open / neutral-loss / hybrid search over ~1e9 public spectra. `max_peak_num` defaults to **unlimited**; noise cut ~1% BPI, not “keep 5 ions”. |
| [ms-entropy API](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html) | `clean_spectra` + `noise_threshold=0.01`, `max_peak_num=None`. Confirms cycle05 `TOP_PEAKS=5` is off-distribution. |
| Huber et al., *Nat Commun* 2023 — [MS2Query](https://www.nature.com/articles/s41467-023-37446-4) | Clean: drop ions <0.1% max intensity; only then cap at **500** lowest-intensity removals. Still keeps two orders of magnitude more peaks than 5. |
| Spec2Vec / MS2DeepScore (MS2Query stack) | Embedding retrieval without precursor prefilter. Out of scope this slot (no weights in the offline kernel). |
| Prior committed cycle docs (`Research/2026-09-17_cycle05_*`, unmerged 2026-09-18/19 PRs #4/#5) | Same scientific conclusion: restore the fragment ladder before retuning mass ppm or entropy mix. |

## Methods to consider

### P0 — Restore `TOP_PEAKS` 5 → 128 (this slot)

**Why.** Cycle05 (`kaggle_id` 56298621, kernel v13) set `TOP_PEAKS=5`. That
truncates `clean_spectrum` after intensity-floor + merge, so entropy/modcos
see only the five strongest ions. Li 2021 showed those weaker ions are what
separate close isomers; Flash Entropy and MS2Query keep tens–hundreds.

**How it raises MRR@25.** More matched fragment / neutral-loss peaks → higher
true-structure similarity, better rank of the correct InChIKey among 25.
Exact-dup poisoning (`spectra_identical`) also needs the real peak vector;
a 5-peak fingerprint over-collides unrelated library rows and under-bans
poisoned `enveda-180` labels.

### P1 — Entropy-dominant hybrid (`ENTROPY_WEIGHT` 0.70)

Unmerged PRs #2/#3 never scored. Keep as the **next** slot after 128-peak
evidence is on the board. Do not stack with this ablation.

### P1 — Structure-level mass + CE aggregation (already on)

`MASS_TOL_PPM=10` / backfill 15, all libraries, `EXCLUDE_EXACT_DUPLICATES=true`
are already in the last submitted kernel. Leave them; isolate `TOP_PEAKS`.

### P2 — Formula → candidate / SIRIUS-style (out of scope)

Needs internet or large in-kernel models. Class-3 de novo is **not** solved
by retrieval. Do not claim otherwise.

### P2 — Spec2Vec / MS2DeepScore embeddings (out of scope)

Would need pretrained weights attached as a dataset. Future kernel, not today.

## Priority table (internet-off notebook)

| Pri | Change | Fit |
| --- | --- | --- |
| P0 | `TOP_PEAKS=128` | One-line config; already in `clean_spectrum` |
| P1 | `ENTROPY_WEIGHT=0.70` | Next slot |
| P1 | OpenAI 429 fallback in `casmi-loop` | Not an MRR ablation; unblocks Actions submit |
| P2 | Embeddings / de novo | Needs extra artifacts |

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 structures are solved by library search.
- Changing mass ppm, entropy mix, or library priors in the same kernel.
- Downloading `train.parquet` locally (not required for this config ablation).
