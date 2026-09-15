# Research — 2026-09-15 cycle01

## Goal

Raise public MRR@25 above our v0.1 score (**0.143**) toward current leaders (~**0.28**).

## Sources reviewed

1. **Li & Fiehn, Nat. Methods (2021)** — Spectral entropy similarity outperforms dot-product for small-molecule ID.  
2. **Li et al., Nat. Methods (2023)** — Flash Entropy Search: scalable entropy similarity for large libraries.  
3. **Watrous / Bittremieux et al., JASMS (2022)** — Modified cosine vs cosine vs neutral-loss alignment; modified cosine remains strong for analogs.  
4. **MS2Query (Nat. Commun. 2023)** — Spec2Vec + MS2Deepscore + RF re-rank; mass prefilter optional for analogs.  
5. **De novo survey (PMC12985711, 2025/26)** — MSNovelist, Spec2Mol, DiffMS etc.; formula conditioning critical; Class-3 still hard.  
6. **CASMI / EPA revisits** — multi-CE aggregation and CFM-ID predicted spectra help when experimental library coverage is incomplete.

## Methods worth considering (priority order for this competition)

| Priority | Method | Why it can lift MRR@25 | Cost / risk |
|----------|--------|------------------------|-------------|
| P0 | **Exclude exact test↔train spectrum duplicates from evidence** | v0.1 shows identical spectra in `enveda-180` whose train labels do **not** match competition GT (perfect library match ⇒ only 0.143). Blind trust of leaked rows actively ranks wrong SMILES #1. | Easy; must still recover true structures via other spectra |
| P0 | **Entropy similarity (+ keep modified cosine)** | Literature: better ID than cosine; diversifies ranking when cosine saturates | Medium; implement offline |
| P0 | **Index all libraries (incl. pluskal_ms2)** | Coverage; NP/public + synthetic space | Index size / runtime |
| P1 | **Structure-level ExactMolWt filter** | Filter by true molecular mass from SMILES, not only spectrum adduct mass | RDKit pass over unique IKs |
| P1 | **CE-aware aggregation** | Reward train hits with CE close to query CE; multi-CE support already partially used | Easy |
| P1 | **Ensemble cleaning views** (floor 0.1%/1%, top-128) | Spec recommends not committing to one view | 2–3× retrieval cost |
| P2 | **MS2Deepscore / Spec2Vec / MS2Query** | SOTA analogue + exact ranking | Heavy deps, offline weights, 9h budget |
| P2 | **Formula prediction → candidate DB** | Needed when structure absent / poisoned labels | Non-trivial |
| P3 | **De novo (DiffMS, MSNovelist)** | Class-3 only; deferred per first-submission spec | High |

## How to improve score (operational recipe)

1. Treat exact-duplicate train rows as **contaminated labels** for ranking (downweight or drop).
2. Rank structures using **non-identical** spectral evidence with hybrid `0.5·entropy + 0.5·modified_cosine`.
3. Expand library coverage; keep timsTOF / enveda prior as soft bonus only.
4. Fill all 25 slots with mass-consistent unique `inchikey14`.
5. Ablate one major factor per submission slot (quota = 5/day).

## Out of scope this cycle

Full MS2Query embedding stack; unconstrained LLM SMILES; training a new deep model from scratch.
