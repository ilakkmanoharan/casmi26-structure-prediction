"""Unit tests for adduct conversion and submission validation."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from casmi26.adducts import (  # noqa: E402
    ADDUCT_RULES,
    H_PLUS,
    infer_neutral_mass,
    mass_within_tol,
    ppm_error,
)
from casmi26.chemistry import inchikey14_from_smiles, is_valid_smiles  # noqa: E402
from casmi26.submission import (  # noqa: E402
    build_submission_frame,
    format_smiles_cell,
    validate_submission,
)


# Ethanol exact mass
ETHANOL_MASS = 46.041864812


@pytest.mark.parametrize(
    "adduct,precursor",
    [
        ("[M+H]+", ETHANOL_MASS + H_PLUS),
        ("[M-H]-", ETHANOL_MASS - H_PLUS),
        ("[M+Na]+", ETHANOL_MASS + ADDUCT_RULES["[M+Na]+"].delta),
        ("[M+K]+", ETHANOL_MASS + ADDUCT_RULES["[M+K]+"].delta),
        ("[M+NH4]+", ETHANOL_MASS + ADDUCT_RULES["[M+NH4]+"].delta),
        ("[M+Cl]-", ETHANOL_MASS + ADDUCT_RULES["[M+Cl]-"].delta),
        ("[M+CH2O2-H]-", ETHANOL_MASS + ADDUCT_RULES["[M+CH2O2-H]-"].delta),
    ],
)
def test_neutral_mass_roundtrip_ethanol(adduct, precursor):
    res = infer_neutral_mass(precursor, adduct)
    assert res.supported
    assert abs(res.neutral_mass - ETHANOL_MASS) < 1e-6
    assert mass_within_tol(res.neutral_mass, ETHANOL_MASS, 1.0)


def test_all_test_adducts_present():
    required = {
        "[M+CH2O2-H]-",
        "[M+Cl]-",
        "[M+H]+",
        "[M+K]+",
        "[M+NH4]+",
        "[M+Na]+",
        "[M-H]-",
    }
    assert required.issubset(set(ADDUCT_RULES))


def test_unsupported_adduct_flagged():
    res = infer_neutral_mass(100.0, "[M+Foo]+")
    assert not res.supported


def test_ppm_error():
    assert abs(ppm_error(100.002, 100.0) - 20.0) < 1e-6


def test_submission_validation_ok():
    sample = pd.DataFrame({"molecule_id": ["m_a", "m_b"], "smiles": ["CCO", "CCO"]})
    preds = {
        "m_a": ["CCO", "CCN"],
        "m_b": ["c1ccccc1"],
    }
    sub = build_submission_frame(preds, sample)
    errors = validate_submission(sub, sample, test_molecule_ids=["m_a", "m_b"])
    assert errors == []


def test_format_dedupes_tautomers_and_invalid():
    # ethanol repeated + invalid
    cell = format_smiles_cell(["CCO", "CCO", "not_a_molecule", "CCN"])
    parts = cell.split(";")
    assert parts[0] == "CCO"
    assert "not_a_molecule" not in parts
    iks = [inchikey14_from_smiles(s) for s in parts]
    assert len(iks) == len(set(iks))


def test_valid_smiles():
    assert is_valid_smiles("CCO")
    assert not is_valid_smiles("C(C")


def test_hybrid_similarity_entropy_weight_interpolates():
    import numpy as np

    from casmi26.config import ENTROPY_WEIGHT
    from casmi26.spectrum import entropy_similarity, hybrid_similarity, modified_cosine

    assert ENTROPY_WEIGHT == 0.70

    mz_a = np.array([50.0, 70.0, 100.0], dtype=np.float32)
    int_a = np.array([0.2, 0.5, 0.8], dtype=np.float32)
    mz_b = np.array([50.02, 90.0, 100.0], dtype=np.float32)
    int_b = np.array([0.3, 0.4, 0.9], dtype=np.float32)
    int_a = int_a / np.linalg.norm(int_a)
    int_b = int_b / np.linalg.norm(int_b)

    cos = modified_cosine(mz_a, int_a, mz_b, int_b, 120.0, 120.0)
    ent = entropy_similarity(mz_a, int_a, mz_b, int_b)
    hybrid = hybrid_similarity(
        mz_a, int_a, mz_b, int_b, 120.0, 120.0, entropy_weight=ENTROPY_WEIGHT
    )
    expected = ENTROPY_WEIGHT * ent + (1.0 - ENTROPY_WEIGHT) * cos
    assert abs(hybrid - expected) < 1e-6

    hybrid55 = hybrid_similarity(
        mz_a, int_a, mz_b, int_b, 120.0, 120.0, entropy_weight=0.55
    )
    if abs(ent - cos) > 1e-6:
        assert abs(hybrid - hybrid55) > 1e-9
