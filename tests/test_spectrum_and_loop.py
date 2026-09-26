"""Peak-ladder restore, OpenAI 429 fallback, and Kaggle credential helper."""

from __future__ import annotations

import json
import stat
import sys
import urllib.error
from email.message import Message
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from casmi26.config import ENTROPY_WEIGHT, TOP_PEAKS  # noqa: E402
from casmi26.spectrum import clean_spectrum  # noqa: E402
from scripts.casmi_loop.chatgpt_spec import FALLBACK_ABLATIONS, _openai_json  # noqa: E402
from scripts.casmi_loop.submit import write_kaggle_credentials  # noqa: E402


def test_top_peaks_restored_to_fragment_ladder():
    assert TOP_PEAKS == 128


def test_clean_spectrum_keeps_requested_top_peaks():
    n = 200
    mz = np.linspace(50.0, 249.0, n)
    inten = np.linspace(0.01, 1.0, n)
    five_mz, _ = clean_spectrum(mz, inten, precursor_mz=260.0, top_peaks=5, intensity_floor=0.0)
    many_mz, _ = clean_spectrum(mz, inten, precursor_mz=260.0, top_peaks=128, intensity_floor=0.0)
    assert len(five_mz) == 5
    assert len(many_mz) == 128
    assert len(many_mz) > len(five_mz)


def test_slot1_fallback_is_top_peaks_128():
    fb = FALLBACK_ABLATIONS[0]
    assert fb["config_patch"] == {"TOP_PEAKS": 128}


def test_entropy_weight_is_li_fiehn_075():
    assert ENTROPY_WEIGHT == 0.75


def test_slot2_fallback_is_entropy_075():
    fb = FALLBACK_ABLATIONS[1]
    assert fb["hypothesis"] == "H-entropy"
    assert fb["config_patch"] == {"ENTROPY_WEIGHT": 0.75}


def test_openai_http_429_returns_none(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-not-a-real-key")

    def boom(_req, timeout=180):  # noqa: ARG001
        raise urllib.error.HTTPError(
            "https://api.openai.com/v1/chat/completions",
            429,
            "Too Many Requests",
            hdrs=Message(),
            fp=None,
        )

    monkeypatch.setattr("scripts.casmi_loop.chatgpt_spec.urllib.request.urlopen", boom)
    assert _openai_json("plan next slot") is None


def test_write_kaggle_credentials_mode_0600(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("KAGGLE_USERNAME", "demo-user")
    monkeypatch.setenv("KAGGLE_KEY", "demo-key")
    monkeypatch.delenv("KAGGLE_API_TOKEN", raising=False)
    assert write_kaggle_credentials() is True
    cred = tmp_path / ".kaggle" / "kaggle.json"
    token = tmp_path / ".kaggle" / "access_token"
    assert cred.is_file()
    assert token.is_file()
    mode = stat.S_IMODE(cred.stat().st_mode)
    assert mode == 0o600
    payload = json.loads(cred.read_text(encoding="utf-8"))
    assert payload["username"] == "demo-user"
    assert payload["key"] == "demo-key"


def test_write_kaggle_credentials_missing_env(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("KAGGLE_USERNAME", raising=False)
    monkeypatch.delenv("KAGGLE_KEY", raising=False)
    monkeypatch.delenv("KAGGLE_API_TOKEN", raising=False)
    assert write_kaggle_credentials() is False
    assert not (tmp_path / ".kaggle" / "kaggle.json").exists()
