"""Plugin remote install trust (ADR-0004)."""
import json

import pytest
from ultra import config, plugins


def test_remote_refused_by_default(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(config, "PLUGINS_DIR", tmp_path / "plugins")
    monkeypatch.delenv("OMEGA_PLUGIN_ALLOW_REMOTE", raising=False)
    with pytest.raises(PermissionError, match="remote plugin install refused"):
        plugins.install("evil/pwn")


def test_remote_allowed_by_env(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(config, "PLUGINS_DIR", tmp_path / "plugins")
    monkeypatch.setenv("OMEGA_PLUGIN_ALLOW_REMOTE", "1")
    assert plugins.remote_install_permitted("any/repo") is True


def test_allowlist_exact_and_glob(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.delenv("OMEGA_PLUGIN_ALLOW_REMOTE", raising=False)
    (tmp_path / "plugins-allowlist.json").write_text(
        json.dumps(["acme/omega-hello", "trusted/*"])
    )
    assert plugins.remote_install_permitted("acme/omega-hello")
    assert plugins.remote_install_permitted("trusted/foo")
    assert not plugins.remote_install_permitted("other/x")


def test_local_install_enabled(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    plug_root = tmp_path / "plugins"
    monkeypatch.setattr(config, "PLUGINS_DIR", plug_root)
    src = tmp_path / "omega-hello"
    src.mkdir()
    (src / "plugin.json").write_text(
        json.dumps({"name": "omega-hello", "runtime": "python", "version": "0.0.1"})
    )
    (src / "plugin.py").write_text("def register(api):\n    pass\n")
    names = plugins.install(str(src))
    assert names == ["omega-hello"]
    assert plugins._enabled("omega-hello") is True
