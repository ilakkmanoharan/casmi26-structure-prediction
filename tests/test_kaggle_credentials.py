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


def test_write_kaggle_credentials_writes_mode_0600(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("KAGGLE_USERNAME", "example-user")
    monkeypatch.setenv("KAGGLE_KEY", "example-key")
    monkeypatch.delenv("KAGGLE_API_TOKEN", raising=False)
    assert write_kaggle_credentials() is True
    json_path = tmp_path / ".kaggle" / "kaggle.json"
    token_path = tmp_path / ".kaggle" / "access_token"
    assert json_path.is_file()
    assert token_path.is_file()
    assert (json_path.stat().st_mode & 0o777) == 0o600
    assert (token_path.stat().st_mode & 0o777) == 0o600
    text = json_path.read_text(encoding="utf-8")
    assert "example-user" in text
    assert "example-key" in text
