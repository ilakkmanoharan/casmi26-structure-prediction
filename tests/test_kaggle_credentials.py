"""Kaggle credential helper (never prints secret values)."""

from __future__ import annotations

from scripts.casmi_loop.submit import write_kaggle_credentials


def test_write_kaggle_credentials_noop_without_env(monkeypatch, tmp_path):
    monkeypatch.delenv("KAGGLE_USERNAME", raising=False)
    monkeypatch.delenv("KAGGLE_KEY", raising=False)
    monkeypatch.delenv("KAGGLE_API_TOKEN", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    assert write_kaggle_credentials() is False
    assert not (tmp_path / ".kaggle" / "kaggle.json").exists()
