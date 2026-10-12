# Hypotheses 2026-10-12_cycle02

## H1 — H-peak-mz (run this slot)

**Statement.** Raising `PEAK_MZ_TOL` from 0.01 → **0.02** Da (MSEntropy `ms2_tolerance_in_da` default) will pair more true-structure fragment ions in `hybrid_similarity`, lifting `best_similarity` for the correct InChIKey14 and raising public MRR@25 versus the current 0.01 window.

**Mechanism.** `casmi26/spectrum.py` `_greedy_match` / `entropy_similarity` / `modified_cosine` all take `tol=cfg.peak_mz_tol`. At 0.01 Da, peaks that differ by typical Orbitrap/QTOF centroiding or library binning (0.012–0.019 Da) miss. 0.02 Da is the Flash Entropy search default; Li/Fiehn 2021 used 0.05 Da.

**Expected MRR direction.** Up vs last scored 0.143 if any public queries fail because fragments do not pair. Still far below the 0.48 CLIST pack unless analogue/forward models land later.

**Failure mode.** A wider window can match decoy fragments and promote wrong IK14s, especially near-isobars already inside the 35 ppm precursor window. `MIN_SIMILARITY=0.05` and the exact-dup ban stay on to limit junk.

## H2 — H-intensity (next unused)

**Statement.** `INTENSITY_FLOOR` 0.001 → 0.01 matches MSEntropy `noise_threshold` and drops 0.1% noise ions that currently dilute entropy. Draft PRs #13–#19, #21, #23, #25. Do not stack with H1 this slot.

## H3 — H-entropy (do not run)

Already live at 0.75. Re-submitting it (Actions slot-2 fallback) wastes a ticket. Retarget that fallback to H1.

## H4 — H-min-sim (later)

`MIN_SIMILARITY` 0.05 → 0.12 (draft PRs #11/#12) would drop weak hits after the match window is literature-aligned. Confounded if run in the same slot as H1.

## This slot

**Run H1 only.** `config_patch = {"PEAK_MZ_TOL": 0.02}`.

Also change `FALLBACK_ABLATIONS[1]` to H-peak-mz so GitHub Actions slot 2 implements the same patch if this Cloud run cannot `competition_submit_code`.
