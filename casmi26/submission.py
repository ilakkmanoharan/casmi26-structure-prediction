"""Submission construction and strict validation."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import pandas as pd

from .chemistry import inchikey14_from_smiles, is_valid_smiles
from .config import MAX_CANDIDATES


REQUIRED_COLUMNS = ("molecule_id", "smiles")


def format_smiles_cell(smiles_list: Sequence[str], max_n: int = MAX_CANDIDATES) -> str:
    cleaned = []
    seen_ik = set()
    for smi in smiles_list:
        if smi is None:
            continue
        s = str(smi).strip()
        if not s or ";" in s:
            continue
        if not is_valid_smiles(s):
            continue
        ik = inchikey14_from_smiles(s)
        if ik is None or ik in seen_ik:
            continue
        seen_ik.add(ik)
        cleaned.append(s)
        if len(cleaned) >= max_n:
            break
    if not cleaned:
        cleaned = ["CCO"]
    return ";".join(cleaned)


def build_submission_frame(
    predictions: Dict[str, Sequence[str]],
    sample_submission: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    for mid in sample_submission["molecule_id"].tolist():
        smiles = predictions.get(mid, ["CCO"])
        rows.append({"molecule_id": mid, "smiles": format_smiles_cell(smiles)})
    return pd.DataFrame(rows, columns=list(REQUIRED_COLUMNS))


def validate_submission(
    sub: pd.DataFrame,
    sample_submission: pd.DataFrame,
    test_molecule_ids: Optional[Iterable[str]] = None,
) -> List[str]:
    """Return list of error strings; empty means OK."""
    errors: List[str] = []
    if list(sub.columns) != list(REQUIRED_COLUMNS):
        errors.append(f"columns must be {REQUIRED_COLUMNS}, got {list(sub.columns)}")
        return errors

    if sub.isnull().any().any():
        errors.append("null values present")

    sample_ids = list(sample_submission["molecule_id"])
    sub_ids = list(sub["molecule_id"])
    if sub_ids != sample_ids:
        if set(sub_ids) != set(sample_ids):
            missing = set(sample_ids) - set(sub_ids)
            extra = set(sub_ids) - set(sample_ids)
            errors.append(f"molecule_id set mismatch missing={len(missing)} extra={len(extra)}")
        else:
            errors.append("molecule_id order differs from sample_submission")

    if sub["molecule_id"].duplicated().any():
        errors.append("duplicate molecule_id rows")

    if test_molecule_ids is not None:
        test_set = set(test_molecule_ids)
        if set(sub_ids) != test_set:
            errors.append("submission ids != test molecule ids")

    for i, row in sub.iterrows():
        cell = row["smiles"]
        if cell is None or str(cell).strip() == "":
            errors.append(f"empty smiles at row {i}")
            continue
        parts = str(cell).split(";")
        if len(parts) > MAX_CANDIDATES:
            errors.append(f">{row['molecule_id']}: >{MAX_CANDIDATES} candidates")
        seen = set()
        for smi in parts:
            if ";" in smi and smi != str(cell):
                errors.append(f"semicolon inside smiles token near {row['molecule_id']}")
            if not is_valid_smiles(smi):
                errors.append(f"{row['molecule_id']}: invalid SMILES {smi!r}")
                break
            ik = inchikey14_from_smiles(smi)
            if ik is None:
                errors.append(f"{row['molecule_id']}: cannot make inchikey14 for {smi!r}")
                break
            if ik in seen:
                errors.append(f"{row['molecule_id']}: duplicate inchikey14 {ik}")
                break
            seen.add(ik)
        if len(errors) > 50:
            errors.append("too many errors; truncated")
            break
    return errors


def write_submission(sub: pd.DataFrame, path) -> None:
    sub.to_csv(path, index=False)
