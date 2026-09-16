"""Tests for loop helpers used by the daily Kaggle submit path."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from casmi26.config import ENTROPY_WEIGHT, EXCLUDE_EXACT_DUPLICATES, RunConfig  # noqa: E402
from scripts.casmi_loop.build_kernel import rebuild_kernel  # noqa: E402
from scripts.casmi_loop.submit import normalize_kernel_status  # noqa: E402


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("ERROR", "ERROR"),
        ("KERNELWORKERSTATUS.ERROR", "ERROR"),
        ("KernelWorkerStatus.ERROR", "ERROR"),
        ("<_status: KernelWorkerStatus.ERROR: 3>", "ERROR"),
        ("COMPLETE", "COMPLETE"),
        ("COMPLETED", "COMPLETE"),
        ("SUCCESS", "COMPLETE"),
        ("RUNNING", "RUNNING"),
        ("INCOMPLETE", "INCOMPLETE"),
        ("", "UNKNOWN"),
        (None, "UNKNOWN"),
    ],
)
def test_normalize_kernel_status(raw, expected):
    assert normalize_kernel_status(raw) == expected


def test_entropy_weight_ablation_is_070():
    assert ENTROPY_WEIGHT == 0.70
    assert RunConfig().entropy_weight == 0.70
    assert EXCLUDE_EXACT_DUPLICATES is True


def test_rebuild_kernel_internet_off_and_rdkit_bootstrap():
    # Rebuild in-repo kernel; assert metadata + bootstrap without needing Kaggle.
    nb_path = rebuild_kernel(title="2026-09-16_cycle01 ENTROPY_WEIGHT=0.70 entropy-dominant hybrid")
    assert nb_path.is_file()
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    ids = [c.get("id") for c in nb["cells"]]
    assert "casmi-embed" in ids
    embed = "".join(nb["cells"][1]["source"])
    assert "_ensure_rdkit" in embed
    assert "ENTROPY_WEIGHT = 0.70" in embed
    meta = json.loads((nb_path.parent / "kernel-metadata.json").read_text(encoding="utf-8"))
    assert meta["enable_internet"] is False
    assert "ilakkmanoharan/rdkit-cp312-wheels-casmi26" in meta["dataset_sources"]
    assert meta["id"] == "ilakkmanoharan/casmi26-retrieval-symbolic-v01"
