"""Path confinement for File API helper."""
from ultra import config
from ultra.gateway import _Handler


class _H(_Handler):
    def __init__(self):
        # bypass SimpleHTTPRequestHandler.__init__
        pass


def test_safe_root_inside(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "ROOT", tmp_path)
    (tmp_path / "a.txt").write_text("x")
    h = _H()
    p = h._safe_root("a.txt")
    assert p is not None
    assert p.name == "a.txt"


def test_safe_root_traversal(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "ROOT", tmp_path)
    h = _H()
    assert h._safe_root("../outside") is None
