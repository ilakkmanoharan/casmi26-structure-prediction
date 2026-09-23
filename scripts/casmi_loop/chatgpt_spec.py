"""Ask ChatGPT for cycle docs + one major ablation; write Research/Analysis/etc."""

from __future__ import annotations

import json
import urllib.error
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

# Deterministic fallbacks when OPENAI_API_KEY is missing or rate-limited.
FALLBACK_ABLATIONS = [
    {
        "hypothesis": "H-peaks-restore",
        "summary": "Restore TOP_PEAKS from 5 to 128 so entropy/modcos keep fragment ladders.",
        "config_patch": {"TOP_PEAKS": 128},
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
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # Actions 35311548455 … 35823205794 died on 429 and skipped Kaggle
        # despite remaining quota.
        print("openai HTTP %s; using deterministic fallback" % exc.code)
        return None
    except urllib.error.URLError as exc:
        print("openai URL error (%s); using deterministic fallback" % exc)
        return None
    text = payload["choices"][0]["message"]["content"]
    return json.loads(text)


def _substantial(path: Path, min_chars: int = 400) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8").strip()
    if len(text) < min_chars:
        return False
    # Ignore empty stubs from older scaffolding.
    if "(filled by agent cycle)" in text and len(text) < 200:
        return False
    return True


def _parse_patch_from_spec(spec_text: str) -> dict[str, Any]:
    """Best-effort extract config_patch JSON from a Spec markdown file."""
    import re

    m = re.search(r"config_patch\s*[:=]\s*(\{.*?\})", spec_text, flags=re.S | re.I)
    if not m:
        m = re.search(r"```json\s*(\{.*?\})\s*```", spec_text, flags=re.S)
    if not m:
        return {}
    try:
        obj = json.loads(m.group(1))
        return obj if isinstance(obj, dict) else {}
    except json.JSONDecodeError:
        return {}


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

    paths = {
        "research": ROOT / "Research" / ("%s_methods.md" % tag),
        "analysis": ROOT / "Analysis" / ("%s_submission.md" % tag),
        "hypothesis": ROOT / "Hypothesis analysis" / ("%s_hypotheses.md" % tag),
        "spec": ROOT / "Specs" / ("%s_next_submission_spec.md" % tag),
    }

    # Prefer Grok Bot / human docs already on main (agent1 steps 1–3).
    if (
        _substantial(paths["research"])
        and _substantial(paths["analysis"])
        and _substantial(paths["hypothesis"])
    ):
        spec_text = (
            paths["spec"].read_text(encoding="utf-8")
            if paths["spec"].is_file()
            else ""
        )
        patch = _parse_patch_from_spec(spec_text)
        if not patch:
            fb = FALLBACK_ABLATIONS[(slot - 1) % len(FALLBACK_ABLATIONS)]
            patch = fb.get("config_patch") or {}
            if not spec_text.strip():
                paths["spec"].write_text(
                    "# Spec %s\n\nReuse Grok Research/Analysis/Hypothesis.\n\n"
                    "config_patch: %s\n" % (tag, json.dumps(patch)),
                    encoding="utf-8",
                )
        print("reusing pre-written cycle docs for", tag)
        return {
            "tag": tag,
            "hypothesis_id": "H-grok",
            "message": "%s grok-docs" % tag,
            "config_patch": patch,
            "domain_prior_boost": None,
            "artifacts": {k: str(v.relative_to(ROOT)) for k, v in paths.items()},
            "notes": "reused_prewritten_docs",
        }

    plan = _openai_json(
        "Plan next CASMI submission slot.\n"
        "Date=%s slot=%s/5 prior_public_score=%s\n\n"
        "Briefing from Kaggle submissions:\n%s\n\n"
        "Return JSON keys: research_md, analysis_md, hypothesis_md, spec_md, "
        "hypothesis_id, message, config_patch (object of EXISTING casmi26/config.py "
        "CONSTANT names only — allowed: MASS_TOL_PPM, MASS_TOL_PPM_BACKFILL, "
        "PEAK_MZ_TOL, TOP_PEAKS, INTENSITY_FLOOR, TOP_K_SPECTRA_PER_QUERY, "
        "TOP_CANDIDATES_PER_SPECTRUM, MIN_SIMILARITY, ENTROPY_WEIGHT, "
        "EXCLUDE_EXACT_DUPLICATES, MAX_CANDIDATES — numeric/bool values), notes. "
        "Do not invent new constant names."
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
