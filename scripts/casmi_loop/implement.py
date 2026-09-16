"""Apply one config ablation and rebuild the Kaggle notebook."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

from .build_kernel import rebuild_kernel
from .config import PACKAGE_DIR

# OpenAI sometimes invents constants; map aliases → real names, skip unknowns.
ALIAS = {
    "EXCLUDE_POISONED_DUPLICATES": "EXCLUDE_EXACT_DUPLICATES",
    "EXCLUDE_EXACT_DUPES": "EXCLUDE_EXACT_DUPLICATES",
    "EXCLUDE_EXACT_DUPLICATE": "EXCLUDE_EXACT_DUPLICATES",
    "ENTROPY_SIM_WEIGHT": "ENTROPY_WEIGHT",
}


def _existing_constants(src: str) -> set[str]:
    return set(re.findall(r"^([A-Z][A-Z0-9_]*)\s*=", src, flags=re.M))


def _replace_assignment(src: str, name: str, value: Any) -> str:
    lit = repr(value)
    pattern = re.compile(r"^(%s\s*=\s*).+$" % re.escape(name), re.M)
    if not pattern.search(src):
        raise KeyError(name)
    return pattern.sub(r"\g<1>%s" % lit, src, count=1)


def _boost_domain_prior(src: str, boosts: dict[str, float]) -> str:
    for key, val in boosts.items():
        pat = re.compile(
            r"([\"']%s[\"']\s*:\s*)([0-9]*\.?[0-9]+)" % re.escape(key)
        )
        src, n = pat.subn(r"\g<1>%s" % repr(val), src, count=1)
        if n == 0:
            print("warn: domain prior key missing:", key)
    return src


def apply_ablation(plan: dict[str, Any]) -> Path:
    cfg_path = PACKAGE_DIR / "config.py"
    src = cfg_path.read_text(encoding="utf-8")
    known = _existing_constants(src)
    patch = plan.get("config_patch") or {}
    if not isinstance(patch, dict):
        raise SystemExit("config_patch must be an object")

    applied: dict[str, Any] = {}
    skipped: list[str] = []
    for name, value in patch.items():
        if not isinstance(name, str):
            skipped.append(repr(name))
            continue
        real = ALIAS.get(name, name)
        if real not in known:
            skipped.append(name)
            continue
        ast.literal_eval(repr(value))
        src = _replace_assignment(src, real, value)
        applied[real] = value

    boosts = plan.get("domain_prior_boost") or {}
    if boosts:
        src = _boost_domain_prior(src, {str(k): float(v) for k, v in boosts.items()})

    if not applied and not boosts:
        # Guaranteed no-op-safe tweak so the slot still changes something.
        if "ENTROPY_WEIGHT" in known:
            src = _replace_assignment(src, "ENTROPY_WEIGHT", 0.65)
            applied["ENTROPY_WEIGHT"] = 0.65
            print("warn: empty/invalid patch; applied default ENTROPY_WEIGHT=0.65")

    cfg_path.write_text(src, encoding="utf-8")
    print("applied config patch", applied, "skipped", skipped, "domain_boost", bool(boosts))
    return rebuild_kernel(title=str(plan.get("message") or "casmi loop"))
