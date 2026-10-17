# Spec 2026-10-17_cycle02

## Goal

One major ablation vs live main (`TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, `PEAK_MZ_TOL=0.01`, `INTENSITY_FLOOR=0.001`):

Raise the relative noise floor to the Flash Entropy / msentropy **1%** default.

## config_patch

```json
{"INTENSITY_FLOOR": 0.01}
```

Also keep `clean_spectrum(..., intensity_floor=0.01)` in sync so callers that use the function default match `casmi26.config`.

## Actions handoff

Change `FALLBACK_ABLATIONS[1]` in `scripts/casmi_loop/chatgpt_spec.py` from H-entropy (`ENTROPY_WEIGHT=0.75`, already live) to:

```json
{
  "hypothesis": "H-intensity",
  "config_patch": {"INTENSITY_FLOOR": 0.01}
}
```

If this PR merges before the next unused hourly casmi-loop slot (**07:00 UTC 2026-10-17**), Actions will reuse these docs (or the new fallback) and **code-submit** kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Kernel

- Rebuild `kaggle_kernel/` from current `casmi26/*.py`
- `enable_internet: false`
- RDKit wheels: `ilakkmanoharan/rdkit-cp312-wheels-casmi26`

## Do not change this slot

`TOP_PEAKS`, `ENTROPY_WEIGHT`, `MASS_TOL_PPM`, `MASS_TOL_PPM_BACKFILL`, `PEAK_MZ_TOL`, `MIN_SIMILARITY`, `EXCLUDE_EXACT_DUPLICATES`, domain priors.

## Success / skip

- **Success:** `kernels push` → COMPLETE → `competition_submit_code` with message `2026-10-17_cycle02 H-intensity`.
- **This Cloud env:** Kaggle secrets absent → implement + PR only; `submitted=false`, `skipped_reason=cloud_missing_kaggle_secrets`.
