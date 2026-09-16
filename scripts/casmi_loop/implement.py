"""Apply one config ablation and rebuild the Kaggle notebook."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

from .build_kernel import rebuild_kernel
from .config import PACKAGE_DIR


def _replace_assignment(src: str, name: str, value: Any) -> str:
    lit = repr(value)
    pattern = re.compile(r"^(%s\s*=\s*).+$" % re.escape(name), re.M)
    if not pattern.search(src):
        raise SystemExit("config constant not found: %s" % name)
    return pattern.sub(r"\g<1>%s" % lit, src, count=1)


def _boost_domain_prior(src: str, boosts: dict[str, float]) -> str:
    # Light-touch: rewrite DOMAIN_PRIOR dict literals for listed keys.
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
    patch = plan.get("config_patch") or {}
    if not isinstance(patch, dict):
        raise SystemExit("config_patch must be an object")
    for name, value in patch.items():
        if not isinstance(name, str) or not name.isidentifier():
            raise SystemExit("bad config key: %r" % name)
        # Validate value is a simple literal
        ast.literal_eval(repr(value))
        src = _replace_assignment(src, name, value)
    boosts = plan.get("domain_prior_boost") or {}
    if boosts:
        src = _boost_domain_prior(src, {str(k): float(v) for k, v in boosts.items()})
    cfg_path.write_text(src, encoding="utf-8")
    print("applied config patch", patch, "domain_boost", bool(boosts))
    return rebuild_kernel(title=str(plan.get("message") or "casmi loop"))
