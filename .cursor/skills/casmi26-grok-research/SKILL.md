---
name: casmi26-grok-research
description: >-
  Grok Bot skill for Enveda CASMI agent1 steps 1–3: web/paper research into
  Research/, prior-submission analysis into Analysis/, and hypotheses into
  Hypothesis analysis/. Use when asked to research CASMI methods, analyze
  Kaggle scores, write hypotheses, or run agent1 research phases.
---

# CASMI Grok Bot — Research / Analysis / Hypothesis

Implements **agent1.md steps 1–3** (not implement/submit). GitHub Actions
(`casmi-loop`) still owns step 5 (Kaggle code submit). You own the write-ups
that improve what the next slot tries.

Repo: `ilakkmanoharan/casmi26-structure-prediction`  
Competition: `enveda-CASMI26-molecule-id-mass-spectra`  
Metric: public **MRR@25** (5 submits / Chicago competition day; day starts **01:00 America/Chicago**)

## Folders (create if missing; commit to git)

| Step | Folder | File pattern |
|------|--------|--------------|
| 1 Research | `Research/` | `YYYY-MM-DD_cycleNN_methods.md` |
| 2 Analysis | `Analysis/` | `YYYY-MM-DD_cycleNN_submission.md` |
| 3 Hypothesis | `Hypothesis analysis/` | `YYYY-MM-DD_cycleNN_hypotheses.md` |

Optional but useful for Actions handoff:

| Spec | `Specs/` | `YYYY-MM-DD_cycleNN_next_submission_spec.md` |

`NN` = next unused cycle for that competition day (read `agent/state.json`).

## Access

- Web search / browser for papers and MS/MS ID methods
- GitHub (`gh`) on this repo — commit + push allowed for the folders above
- Kaggle CLI or API if credentials exist on the Bot computer (`~/.kaggle/kaggle.json`); otherwise use public submission pages + committed `Analysis/` / `agent/state.json`
- Never print secrets

## Mandatory order (one cycle)

### 1. Research (`agent1` step 1)

Search the internet and read papers on techniques that can raise **MRR@25** for structure ID from MS/MS (entropy similarity, modified cosine, library search, MS2Query / Spec2Vec / MS2Deepscore, formula→candidate, CE aggregation, exact-dup contamination, etc.).

Write `Research/YYYY-MM-DD_cycleNN_methods.md` covering:

- Sources reviewed (papers / posts with links)
- Methods to consider, **why**, and **how** each could improve score
- Priority table (P0/P1/P2) fit for a **notebook-only, internet-off** Kaggle kernel
- Explicit out-of-scope items for this cycle

### 2. Analysis (`agent1` step 2)

Pull prior submission logs / scores:

```bash
kaggle competitions submissions -c enveda-CASMI26-molecule-id-mass-spectra
```

Also read `agent/state.json`, prior `Analysis/`, and any `outputs/` notes if present.

Write `Analysis/YYYY-MM-DD_cycleNN_submission.md`:

- Recent public scores + messages
- Why score is low (cite evidence; known issue: exact test↔train dups in `enveda-180` with train labels ≠ GT)
- Concrete improvements for the next slot

### 3. Hypothesis (`agent1` step 3)

Using Research + Analysis, write
`Hypothesis analysis/YYYY-MM-DD_cycleNN_hypotheses.md`:

- 2–4 testable hypotheses (H1, H2, …)
- Which **one** major ablation to run this slot
- Expected MRR direction and failure mode

### 4. Handoff (recommended)

Write a short `Specs/YYYY-MM-DD_cycleNN_next_submission_spec.md` with an actionable
`config_patch` using **only** existing `casmi26/config.py` constants:
`MASS_TOL_PPM`, `MASS_TOL_PPM_BACKFILL`, `PEAK_MZ_TOL`, `TOP_PEAKS`,
`INTENSITY_FLOOR`, `TOP_K_SPECTRA_PER_QUERY`, `TOP_CANDIDATES_PER_SPECTRUM`,
`MIN_SIMILARITY`, `ENTROPY_WEIGHT`, `EXCLUDE_EXACT_DUPLICATES`, `MAX_CANDIDATES`.

Then commit and push:

```bash
git add Research Analysis "Hypothesis analysis" Specs
git -c user.name="ilakk manoharan" -c user.email="28582192+ilakkmanoharan@users.noreply.github.com" commit -m "Add cycleNN Research/Analysis/Hypothesis from Grok Bot"
git push origin HEAD
```

To let Actions implement + submit from your docs:

```bash
python3 scripts/casmi_loop/check_and_dispatch.py --dispatch
```

(`casmi-loop` will reuse substantial pre-written cycle docs when present.)

## Approval boundary

- **Allowed:** create/update markdown under `Research/`, `Analysis/`, `Hypothesis analysis/`, `Specs/`; commit/push those paths; read Kaggle submission list; dispatch `casmi-loop` after docs are pushed.
- **Ask first:** editing `casmi26/` code yourself, changing secrets, force-submitting after quota full, deleting prior cycle history.

## Suggested routine

> Every 90 minutes between 01:00 and 10:00 America/Chicago, if Chicago
> competition-day submissions &lt; 5 and no casmi-loop run is in progress:
> run casmi26-grok-research for the next cycle (Research → Analysis →
> Hypothesis analysis → Spec), commit/push, then dispatch casmi-loop.
> If quota is full or a run is in progress, post a short status only.

Pair with `casmi26-grok-watchdog` for failure recovery, or combine both skills on one Bot.

## Quality bar

- Cite sources with links
- Prefer one major ablation per cycle
- Do not claim Class-3 de novo is solved by retrieval alone
- Notebook-only: never recommend CSV-only `competitions submit`
