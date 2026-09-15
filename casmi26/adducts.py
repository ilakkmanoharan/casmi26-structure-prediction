"""Explicit adduct → neutral-mass conversion rules.

All supported test-set adducts are unit-tested. Unsupported adducts raise and are logged
by callers; they are never silently ignored.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

# IUPAC / CODATA-ish monoisotopic masses
MASS: Dict[str, float] = {
    "e": 0.000548579909065,  # electron
    "H": 1.00782503224,
    "C": 12.0,
    "N": 14.00307400443,
    "O": 15.99491461957,
    "Na": 22.9897692820,
    "Cl": 34.968852682,  # 35Cl
    "K": 38.9637064864,
}

H_PLUS = MASS["H"] - MASS["e"]  # 1.00727645233
NA_PLUS = MASS["Na"] - MASS["e"]
K_PLUS = MASS["K"] - MASS["e"]
NH4_PLUS = MASS["N"] + 4 * MASS["H"] - MASS["e"]
CL_MINUS = MASS["Cl"] + MASS["e"]
# [M+CH2O2-H]- ≡ [M+HCOO]- : adduct ion mass contribution ≈ CHO2 + e for m/z of anion
CHO2 = MASS["C"] + MASS["H"] + 2 * MASS["O"]  # formyl/formate heavy-atom+H skeleton
HCOO_MINUS = CHO2 + MASS["e"]


@dataclass(frozen=True)
class AdductRule:
    name: str
    charge: int
    polarity: str  # "positive" | "negative"
    # ion_mz = (neutral_mass + delta) / abs(charge)
    # so neutral_mass = ion_mz * abs(charge) - delta
    delta: float
    description: str

    def neutral_mass(self, precursor_mz: float) -> float:
        if self.charge == 0:
            raise ValueError(f"Invalid charge for adduct {self.name}")
        return precursor_mz * abs(self.charge) - self.delta

    def precursor_mz(self, neutral_mass: float) -> float:
        return (neutral_mass + self.delta) / abs(self.charge)


# delta such that: precursor_mz ≈ (M + delta) / |z|
# [M+H]+ : precursor = M + H+  => delta = +H_PLUS
# [M-H]- : precursor = M - H+  => delta = -H_PLUS
# [M+Na]+ : precursor = M + Na+ => delta = +NA_PLUS
# [M+Cl]- : precursor = M + Cl- => delta = +CL_MINUS
# [M+CH2O2-H]- : precursor = M + HCOO- => delta = +HCOO_MINUS
ADDUCT_RULES: Dict[str, AdductRule] = {
    "[M+H]+": AdductRule("[M+H]+", 1, "positive", H_PLUS, "protonated"),
    "[M-H]-": AdductRule("[M-H]-", -1, "negative", -H_PLUS, "deprotonated"),
    "[M+Na]+": AdductRule("[M+Na]+", 1, "positive", NA_PLUS, "sodium adduct"),
    "[M+K]+": AdductRule("[M+K]+", 1, "positive", K_PLUS, "potassium adduct"),
    "[M+NH4]+": AdductRule("[M+NH4]+", 1, "positive", NH4_PLUS, "ammonium adduct"),
    "[M+Cl]-": AdductRule("[M+Cl]-", -1, "negative", CL_MINUS, "chloride adduct"),
    "[M+CH2O2-H]-": AdductRule(
        "[M+CH2O2-H]-", -1, "negative", HCOO_MINUS, "formate adduct"
    ),
    # Extra training adducts (used when indexing train; not required in test)
    "[M]+": AdductRule("[M]+", 1, "positive", -MASS["e"], "radical cation"),
    "[2M+H]+": AdductRule("[2M+H]+", 1, "positive", H_PLUS, "dimer protonated"),
    "[2M-H]-": AdductRule("[2M-H]-", -1, "negative", -H_PLUS, "dimer deprotonated"),
    "[2M+Na]+": AdductRule("[2M+Na]+", 1, "positive", NA_PLUS, "dimer sodium"),
    "[2M+CH2O2-H]-": AdductRule(
        "[2M+CH2O2-H]-", -1, "negative", HCOO_MINUS, "dimer formate"
    ),
}

DIMER_ADDUCTS = {"[2M+H]+", "[2M-H]-", "[2M+Na]+", "[2M+CH2O2-H]-"}


@dataclass
class NeutralMassResult:
    adduct: str
    precursor_mz: float
    neutral_mass: float
    charge: int
    polarity: str
    supported: bool
    note: str = ""
    monomer_mass: Optional[float] = None  # for dimers: estimated monomer mass


def parse_adduct(adduct: str) -> AdductRule:
    if adduct not in ADDUCT_RULES:
        raise KeyError(f"Unsupported adduct: {adduct!r}")
    return ADDUCT_RULES[adduct]


def infer_neutral_mass(precursor_mz: float, adduct: str) -> NeutralMassResult:
    if adduct not in ADDUCT_RULES:
        return NeutralMassResult(
            adduct=adduct,
            precursor_mz=float(precursor_mz),
            neutral_mass=float("nan"),
            charge=0,
            polarity="unknown",
            supported=False,
            note="unsupported_adduct",
        )
    rule = ADDUCT_RULES[adduct]
    nm = rule.neutral_mass(float(precursor_mz))
    monomer = None
    note = ""
    if adduct in DIMER_ADDUCTS:
        # For [2M+X], ion mass ≈ 2M + delta => monomer ≈ nm/2 is wrong because
        # our delta is applied once. Correct: precursor = 2*M + delta => M = (p - delta)/2
        monomer = (float(precursor_mz) - rule.delta) / 2.0
        note = "dimer"
        nm = monomer  # treat as monomer mass for structure retrieval
    return NeutralMassResult(
        adduct=adduct,
        precursor_mz=float(precursor_mz),
        neutral_mass=float(nm),
        charge=rule.charge,
        polarity=rule.polarity,
        supported=True,
        note=note,
        monomer_mass=monomer,
    )


def ppm_error(observed: float, expected: float) -> float:
    if expected == 0 or expected != expected:
        return float("inf")
    return (observed - expected) / expected * 1e6


def mass_within_tol(observed: float, expected: float, tol_ppm: float) -> bool:
    return abs(ppm_error(observed, expected)) <= tol_ppm


def polarity_compatible(adduct: str, ionization_mode: Optional[str]) -> Tuple[bool, str]:
    if adduct not in ADDUCT_RULES:
        return False, "unsupported_adduct"
    rule = ADDUCT_RULES[adduct]
    if ionization_mode is None or ionization_mode == "" or ionization_mode != ionization_mode:
        return True, "mode_missing"
    mode = str(ionization_mode).lower()
    if mode not in ("positive", "negative"):
        return True, "mode_unknown"
    if mode != rule.polarity:
        return False, "polarity_mismatch"
    return True, "ok"
