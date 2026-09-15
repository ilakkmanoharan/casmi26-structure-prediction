"""RDKit standardization helpers aligned with competition identity rules."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional, Tuple

from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import Descriptors


_TE = rdMolStandardize.TautomerEnumerator()


def mol_from_smiles(smiles: str) -> Optional[Chem.Mol]:
    if smiles is None:
        return None
    mol = Chem.MolFromSmiles(str(smiles))
    if mol is None:
        return None
    try:
        Chem.SanitizeMol(mol)
    except Exception:
        return None
    return mol


def tautomer_canonical_smiles(smiles: str) -> Optional[str]:
    mol = mol_from_smiles(smiles)
    if mol is None:
        return None
    try:
        canon = _TE.Canonicalize(mol)
        return Chem.MolToSmiles(canon, isomericSmiles=False)
    except Exception:
        try:
            return Chem.MolToSmiles(mol, isomericSmiles=False)
        except Exception:
            return None


def inchikey14_from_smiles(smiles: str, tautomer_canonical: bool = False) -> Optional[str]:
    mol = mol_from_smiles(smiles)
    if mol is None:
        return None
    try:
        if tautomer_canonical:
            mol = _TE.Canonicalize(mol)
        ik = Chem.MolToInchiKey(mol)
    except Exception:
        return None
    if not ik or len(ik) < 14:
        return None
    return ik[:14]


def exact_mass_from_smiles(smiles: str) -> Optional[float]:
    mol = mol_from_smiles(smiles)
    if mol is None:
        return None
    try:
        return float(Descriptors.ExactMolWt(mol))
    except Exception:
        return None


@lru_cache(maxsize=300_000)
def standardize_record(smiles: str) -> Tuple[Optional[str], Optional[str], Optional[float]]:
    """Return (canonical_smiles, inchikey14, exact_mass)."""
    mol = mol_from_smiles(smiles)
    if mol is None:
        return None, None, None
    try:
        canon_mol = _TE.Canonicalize(mol)
    except Exception:
        canon_mol = mol
    try:
        canon_smi = Chem.MolToSmiles(canon_mol, isomericSmiles=False)
        ik = Chem.MolToInchiKey(canon_mol)
        mass = float(Descriptors.ExactMolWt(canon_mol))
    except Exception:
        return None, None, None
    if not ik or len(ik) < 14:
        return None, None, None
    return canon_smi, ik[:14], mass


def is_valid_smiles(smiles: str) -> bool:
    return mol_from_smiles(smiles) is not None
