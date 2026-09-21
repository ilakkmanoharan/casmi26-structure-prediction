"""OpenAI 429/5xx must not abort casmi-loop before Kaggle submit."""

from __future__ import annotations

import io
import urllib.error

from scripts.casmi_loop import chatgpt_spec


def test_openai_http_429_returns_none(monkeypatch):
    monkeypatch.setattr(chatgpt_spec, "secret", lambda _name: "dummy-key")

    def boom(_req, timeout=180):
        raise urllib.error.HTTPError(
            "https://api.openai.com/v1/chat/completions",
            429,
            "Too Many Requests",
            hdrs=None,
            fp=io.BytesIO(b""),
        )

    monkeypatch.setattr(chatgpt_spec.urllib.request, "urlopen", boom)
    assert chatgpt_spec._openai_json("plan next slot") is None


def test_openai_url_error_returns_none(monkeypatch):
    monkeypatch.setattr(chatgpt_spec, "secret", lambda _name: "dummy-key")

    def boom(_req, timeout=180):
        raise urllib.error.URLError("timed out")

    monkeypatch.setattr(chatgpt_spec.urllib.request, "urlopen", boom)
    assert chatgpt_spec._openai_json("plan next slot") is None
