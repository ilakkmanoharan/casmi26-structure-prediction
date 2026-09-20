"""Spectrum cleaning / config guards for retrieval ablations."""

from __future__ import annotations

import numpy as np

from casmi26.config import TOP_PEAKS
from casmi26.spectrum import clean_spectrum


def test_top_peaks_restored_from_cycle05_cap():
    """Cycle05 set TOP_PEAKS=5; entropy/Flash Entropy keep far more than 5 ions."""
    assert TOP_PEAKS == 128
    assert TOP_PEAKS >= 64


def test_clean_spectrum_keeps_more_than_five_peaks():
    n = 40
    mz = np.linspace(50.0, 400.0, n)
    inten = np.linspace(0.05, 1.0, n)
    out_mz, out_int = clean_spectrum(
        mz,
        inten,
        precursor_mz=450.0,
        intensity_floor=0.001,
        top_peaks=TOP_PEAKS,
        sqrt_intensity=True,
    )
    assert len(out_mz) == n
    assert len(out_mz) > 5
    assert out_mz.shape == out_int.shape


def test_clean_spectrum_respects_small_top_peaks_cap():
    mz = np.linspace(50.0, 400.0, 40)
    inten = np.linspace(0.05, 1.0, 40)
    out_mz, _ = clean_spectrum(mz, inten, precursor_mz=450.0, top_peaks=5)
    assert len(out_mz) == 5
