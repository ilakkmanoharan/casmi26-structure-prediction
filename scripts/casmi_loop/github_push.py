"""Commit cycle artifacts and push to GitHub (Actions GITHUB_TOKEN)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .config import ROOT, STATE_FILE

ORIGIN_URL = "https://github.com/ilakkmanoharan/casmi26-structure-prediction.git"
ORIGIN_NAME = "origin"
BRANCH = "main"
AUTHOR_NAME = "ilakk manoharan"
AUTHOR_EMAIL = "28582192+ilakkmanoharan@users.noreply.github.com"


class GitPushError(RuntimeError):
    pass


def _run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if check and proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise GitPushError("%s failed: %s" % (" ".join(args), err[:800]))
    return proc


def _ensure_origin() -> None:
    remotes = _run(["git", "remote"], check=False).stdout.split()
    if ORIGIN_NAME not in remotes:
        _run(["git", "remote", "add", ORIGIN_NAME, ORIGIN_URL])
        return
    current = _run(["git", "remote", "get-url", ORIGIN_NAME]).stdout.strip()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and "github.com" in current:
        auth_url = (
            "https://x-access-token:%s@github.com/ilakkmanoharan/casmi26-structure-prediction.git"
            % token
        )
        _run(["git", "remote", "set-url", ORIGIN_NAME, auth_url])
    elif "ilakkmanoharan/casmi26-structure-prediction" not in current:
        _run(["git", "remote", "set-url", ORIGIN_NAME, ORIGIN_URL])


def _safe_rel(path: Path) -> str | None:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return None


def push_paths(paths: list[Path], message: str) -> dict:
    if not (ROOT / ".git").exists():
        raise GitPushError("not a git repo: %s" % ROOT)
    _ensure_origin()
    _run(["git", "fetch", ORIGIN_NAME], check=False)
    _run(["git", "pull", "--rebase", ORIGIN_NAME, BRANCH], check=False)

    rels: list[str] = []
    for path in paths:
        rel = _safe_rel(path)
        if rel and path.exists():
            rels.append(rel)
    if STATE_FILE.exists():
        rels.append(_safe_rel(STATE_FILE) or "agent/state.json")
    # always include package + kernel when present
    for extra in ("casmi26", "kaggle_kernel"):
        if (ROOT / extra).exists():
            rels.append(extra)
    rels = sorted(set(r for r in rels if r))
    if not rels:
        raise GitPushError("nothing to add")

    _run(["git", "add", "--"] + rels)
    staged = _run(["git", "diff", "--cached", "--quiet"], check=False)
    committed = False
    if staged.returncode != 0:
        _run(
            [
                "git",
                "-c",
                "user.name=%s" % AUTHOR_NAME,
                "-c",
                "user.email=%s" % AUTHOR_EMAIL,
                "commit",
                "-m",
                message,
            ]
        )
        committed = True
    _run(["git", "push", "-u", ORIGIN_NAME, "HEAD:%s" % BRANCH])
    sha = _run(["git", "rev-parse", "HEAD"]).stdout.strip()
    print("pushed %s (%s)" % (sha[:8], "new commit" if committed else "already committed"))
    return {"sha": sha, "committed": committed, "paths": rels}
