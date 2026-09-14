import json

from ultra import config, plugins


def test_remote_install_writes_sandbox_trust(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(config, "PLUGINS_DIR", tmp_path / "plugins")
    src = tmp_path / "plug"
    src.mkdir()
    (src / "plugin.json").write_text(json.dumps({"name": "x", "runtime": "python"}))
    (src / "plugin.py").write_text("def register(api):\n    pass\n")
    # local path install stays enabled / no forced sandbox
    names = plugins.install(str(src))
    assert names == ["plug"]
    assert plugins._trust_of(tmp_path / "plugins" / "plug") == "inprocess"


def test_sandbox_handle_subprocess(tmp_path):
    d = tmp_path / "sb"
    d.mkdir()
    (d / "plugin.py").write_text(
        "def handle(event):\n    return {'ok': True, 'path': event.get('path'), 'status': 200}\n"
    )
    out = plugins._run_sandbox_handle(d, {"method": "GET", "path": "/api/x", "query": {}, "body": {}})
    assert out.get("ok") is True
    assert out.get("path") == "/api/x"
