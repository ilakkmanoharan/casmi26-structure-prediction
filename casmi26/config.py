"""Global configuration for the first retrieval submission."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
ARTIFACT_DIR = ROOT / "artifacts"

SEED = 42
MAX_CANDIDATES = 25
MASS_TOL_PPM = 35.0
MASS_TOL_PPM_BACKFILL = 80.0
PEAK_MZ_TOL = 0.01
TOP_PEAKS = 128
INTENSITY_FLOOR = 0.001
MAX_PEAKS_ABOVE_PRECURSOR_DA = 2.0
TOP_K_SPECTRA_PER_QUERY = 120
TOP_CANDIDATES_PER_SPECTRUM = 25
MIN_SIMILARITY = 0.08
ENTROPY_WEIGHT = 0.6
EXCLUDE_EXACT_DUPLICATES = True

# Aggregation weights (normalized features). Tuned for MRR@25 orientation.
WEIGHTS: Dict[str, float] = {
    "best_similarity": 1.00,
    "mean_top_k_similarity": 0.35,
    "support_log": 0.25,
    "ce_coverage": 0.10,
    "adduct_coverage": 0.10,
    "domain_prior": 0.20,
    "quality": 0.10,
    "mass_error": 0.30,
    "contradiction": 0.50,
}

DOMAIN_PRIOR: Dict[str, float] = {
    "enveda-np-examples": 1.00,
    "enveda-180": 0.95,
    "gnps": 0.72,
    "riken": 0.72,
    "massbank": 0.65,
    "mona": 0.65,
    "msdial": 0.60,
    "spectraverse": 0.60,
    "pluskal_ms2": 0.45,
    "drug_plus": 0.40,
    "masaryk": 0.40,
}

PREFERRED_LIBS: List[str] = [
    "enveda-np-examples",
    "enveda-180",
    "gnps",
    "riken",
    "massbank",
    "mona",
    "msdial",
    "spectraverse",
]


@dataclass
class RunConfig:
    mass_tol_ppm: float = MASS_TOL_PPM
    mass_tol_ppm_backfill: float = MASS_TOL_PPM_BACKFILL
    peak_mz_tol: float = PEAK_MZ_TOL
    top_peaks: int = TOP_PEAKS
    intensity_floor: float = INTENSITY_FLOOR
    top_k_spectra: int = TOP_K_SPECTRA_PER_QUERY
    top_candidates_per_spectrum: int = TOP_CANDIDATES_PER_SPECTRUM
    min_similarity: float = MIN_SIMILARITY
    max_candidates: int = MAX_CANDIDATES
    seed: int = SEED
    use_neutral_loss: bool = True
    prefer_same_mode: bool = True
    entropy_weight: float = ENTROPY_WEIGHT
    exclude_exact_duplicates: bool = EXCLUDE_EXACT_DUPLICATES
    weights: Dict[str, float] = field(default_factory=lambda: dict(WEIGHTS))
    domain_prior: Dict[str, float] = field(default_factory=lambda: dict(DOMAIN_PRIOR))

    def to_dict(self) -> dict:
        return asdict(self)
