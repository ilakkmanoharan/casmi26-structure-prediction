"""Ask ChatGPT for cycle docs + one major ablation; write Research/Analysis/etc."""

from __future__ import annotations

import json
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

from .config import ROOT, secret, tag_for

SYSTEM = (
    "You are the strategist for Enveda CASMI 2026 (molecule ID from MS/MS). "
    "Metric is public MRR@25. Notebook-only Kaggle submit. Prefer one major ablation "
    "per submission. Known failure: exact test↔train spectrum duplicates in enveda-180 "
    "with train labels ≠ GT. Prefer entropy/modcos hybrid, exclude exact-dup IKs, "
    "broader libraries, structure-level mass filters. Return strict JSON only."
)

# Deterministic fallbacks when OPENAI_API_KEY is missing.
FALLBACK_ABLATIONS = [
    {
        "hypothesis": "H-entropy",
        "summary": "Raise entropy_weight toward entropy similarity dominance.",
        "config_patch": {"ENTROPY_WEIGHT": 0.70},
    },
    {
        "hypothesis": "H-mass-tight",
        "summary": "Tighten primary mass window to reduce false library hits.",
        "config_patch": {"MASS_TOL_PPM": 15.0, "MASS_TOL_PPM_BACKFILL": 40.0},
    },
    {
        "hypothesis": "H-mass-wide",
        "summary": "Widen mass window + more neighbors for sparse queries.",
        "config_patch": {
            "MASS_TOL_PPM": 35.0,
            "MASS_TOL_PPM_BACKFILL": 80.0,
            "TOP_K_SPECTRA_PER_QUERY": 120,
        },
    },
    {
        "hypothesis": "H-peaks",
        "summary": "Keep more peaks and slightly lower min similarity.",
        "config_patch": {"TOP_PEAKS": 160, "MIN_SIMILARITY": 0.05},
    },
    {
        "hypothesis": "H-domain",
        "summary": "Boost natural-product libraries in domain_prior.",
        "config_patch": {},
        "domain_prior_boost": {"enveda-np-examples": 1.0, "enveda-180": 1.0, "gnps": 0.85},
    },
]


def _openai_json(user: str) -> dict[str, Any] | None:
    key = secret("OPENAI_API_KEY")
    if not key:
        return None
    body = {
        "model": "gpt-4o",
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    text = payload["choices"][0]["message"]["content"]
    return json.loads(text)


def write_cycle_docs(
    *,
    day: date,
    slot: int,
    briefing: str,
    prior_score: float | None,
) -> dict[str, Any]:
    tag = tag_for(day, slot)
    for name in ("Research", "Analysis", "Hypothesis analysis", "Specs"):
        (ROOT / name).mkdir(parents=True, exist_ok=True)

    plan = _openai_json(
        "Plan next CASMI submission slot.\n"
        "Date=%s slot=%s/5 prior_public_score=%s\n\n"
        "Briefing from Kaggle submissions:\n%s\n\n"
        "Return JSON keys: research_md, analysis_md, hypothesis_md, spec_md, "
        "hypothesis_id, message, config_patch (object of casmi26/config.py CONSTANT "
        "names to new numeric/bool values), notes."
        % (day.isoformat(), slot, prior_score, briefing[:12000])
    )
    if plan is None:
        fb = FALLBACK_ABLATIONS[(slot - 1) % len(FALLBACK_ABLATIONS)]
        plan = {
            "research_md": "# Research %s\n\nFallback ablation (no OPENAI_API_KEY).\n\n%s\n"
            % (tag, fb["summary"]),
            "analysis_md": "# Analysis %s\n\nPrior score: %s\n\n%s\n"
            % (tag, prior_score, briefing[:4000]),
            "hypothesis_md": "# Hypotheses %s\n\n- %s: %s\n"
            % (tag, fb["hypothesis"], fb["summary"]),
            "spec_md": "# Spec %s\n\nApply config_patch: %s\n"
            % (tag, json.dumps(fb.get("config_patch") or {})),
            "hypothesis_id": fb["hypothesis"],
            "message": "%s %s" % (tag, fb["hypothesis"]),
            "config_patch": fb.get("config_patch") or {},
            "domain_prior_boost": fb.get("domain_prior_boost"),
            "notes": "openai_missing_fallback",
        }

    paths = {
        "research": ROOT / "Research" / ("%s_methods.md" % tag),
        "analysis": ROOT / "Analysis" / ("%s_submission.md" % tag),
        "hypothesis": ROOT / "Hypothesis analysis" / ("%s_hypotheses.md" % tag),
        "spec": ROOT / "Specs" / ("%s_next_submission_spec.md" % tag),
    }
    paths["research"].write_text(str(plan.get("research_md") or "# Research\n"), encoding="utf-8")
    paths["analysis"].write_text(str(plan.get("analysis_md") or "# Analysis\n"), encoding="utf-8")
    paths["hypothesis"].write_text(
        str(plan.get("hypothesis_md") or "# Hypotheses\n"), encoding="utf-8"
    )
    paths["spec"].write_text(str(plan.get("spec_md") or "# Spec\n"), encoding="utf-8")

    return {
        "tag": tag,
        "hypothesis_id": plan.get("hypothesis_id") or "H-auto",
        "message": plan.get("message") or ("%s auto" % tag),
        "config_patch": plan.get("config_patch") or {},
        "domain_prior_boost": plan.get("domain_prior_boost"),
        "artifacts": {k: str(v.relative_to(ROOT)) for k, v in paths.items()},
        "notes": plan.get("notes"),
    }
