# Hypotheses — 2026-10-28 cycle02

## H1 (this slot) — MIN_SIMILARITY 0.05 → 0.12

**Claim.** Raising the library-hit admission floor from 0.05 to 0.12 drops low-confidence entropy/modcos decoys from `top_k`, so mid-score true InChIKey14s that currently sit past rank 25 move into the scored window and public MRR@25 rises.

**Mechanism.** `retrieve.py` only appends a library spectrum when `sim >= cfg.min_similarity`. At 0.05, hybrid scores that Li/Fiehn 2021 would treat as FDR-dominated still occupy the 120-spectrum / 25-candidate lists. 0.12 is a conservative step (not 0.75) so sparse 2–4 peak queries can still emit a list.

**Expected MRR direction.** Up vs 0.143 if decoy packing is the bottleneck among *in-library* queries. Unchanged if the public split is dominated by poisoned exact-dups / absent structures (Class-3). Unlikely to *drop* unless many true hits currently score in (0.05, 0.12) — possible on very sparse spectra.

**Failure mode.** Empty candidate lists on noisy/sparse queries → more placeholder / fallback SMILES → MRR down. Mitigant: keep mass-wide 35/80 backfill and `TOP_K=120`; do not jump to 0.75.

## H2 — TOP_PEAKS 128 → 160 (next unused)

**Claim.** After the 1% intensity floor, Flash Entropy prefers not to hard-cap the ladder. 160 peaks may recover weak diagnostic ions.

**Why not now.** One major factor per slot. Do not stack on H1. Slot-3 fallback after this cycle (`TOP_PEAKS=160` only — do **not** reset `MIN_SIMILARITY`).

## H3 — Replay PEAK_MZ_TOL=0.02 (reject)

Already live since 10-24/10-25 Cloud H-peak-mz merged. Actions 10-27 cycle02/03 already wasted two tickets on this. Slot-2 on main still points here — that is the bug this cycle fixes in `FALLBACK_ABLATIONS`.

## H4 — Analog / MS2Query channel (later)

Literature and public notebooks (~0.43–0.46) show analog search lifts recall when the exact structure is missing. Out of scope for a one-constant notebook slot; internet off; weights too large.

## This slot

Run **H1 only**. Hypothesis id: `H-min-sim`.
