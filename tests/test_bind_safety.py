"""Gateway bind safety."""

import pytest
from ultra import config


def test_loopback_ok(monkeypatch):
    monkeypatch.delenv("OMEGA_GATEWAY_ALLOW_REMOTE", raising=False)
    monkeypatch.delenv("OMEGA_GATEWAY_HOST", raising=False)
    assert config.gateway_host("127.0.0.1") == "127.0.0.1"
    assert config.gateway_host("localhost") == "localhost"


def test_remote_refused(monkeypatch):
    monkeypatch.delenv("OMEGA_GATEWAY_ALLOW_REMOTE", raising=False)
    with pytest.raises(RuntimeError, match="non-loopback"):
        config.gateway_host("0.0.0.0")


def test_remote_allowed(monkeypatch):
    monkeypatch.setenv("OMEGA_GATEWAY_ALLOW_REMOTE", "1")
    assert config.gateway_host("0.0.0.0") == "0.0.0.0"
