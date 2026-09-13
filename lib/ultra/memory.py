"""Working memory (0.4) — session-scoped turns under OMEGA_DATA/memory/working.

Episodic / Semantic / Procedural / User-Project namespaces are reserved dirs
only; no fake retrieval yet.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from . import config

_SESSION_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")
_MAX_TURNS = 200


def _safe_session(session_id: str) -> str:
    sid = (session_id or "").strip()
    if not _SESSION_RE.match(sid):
        raise ValueError(
            "session_id must be 1–128 chars of [A-Za-z0-9_.:-]"
        )
    return sid


def ensure_layout() -> None:
    """Create memory namespace directories (working + reserved stubs)."""
    for name in ("working", "episodic", "semantic", "procedural", "user_project"):
        (config.MEMORY_DIR / name).mkdir(parents=True, exist_ok=True)
    readme = config.MEMORY_DIR / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Omega memory namespaces\n\n"
            "- `working/` — session turns (implemented 0.4)\n"
            "- `episodic/`, `semantic/`, `procedural/`, `user_project/` — reserved\n",
            encoding="utf-8",
        )


def _path(session_id: str) -> Path:
    return config.MEMORY_WORKING_DIR / f"{_safe_session(session_id)}.jsonl"


def append_turn(
    session_id: str,
    *,
    role: str,
    content: str,
    source: str = "api",
    confidence: float = 1.0,
    request_id: str = "",
    meta: dict | None = None,
) -> dict:
    """Append one turn with provenance. Returns the stored record."""
    ensure_layout()
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "role": role,
        "content": content,
        "provenance": {
            "source": source,
            "confidence": float(confidence),
            "request_id": request_id or "",
        },
        "meta": meta or {},
    }
    path = _path(session_id)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    # trim
    turns = load_turns(session_id)
    if len(turns) > _MAX_TURNS:
        keep = turns[-_MAX_TURNS:]
        path.write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep),
            encoding="utf-8",
        )
        return keep[-1]
    return rec


def load_turns(session_id: str, limit: int = 50) -> list[dict]:
    path = _path(session_id)
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            continue
    if limit and limit > 0:
        return rows[-limit:]
    return rows


def forget(session_id: str) -> bool:
    path = _path(session_id)
    if path.exists():
        path.unlink()
        return True
    return False


def list_sessions() -> list[str]:
    ensure_layout()
    out = []
    for p in sorted(config.MEMORY_WORKING_DIR.glob("*.jsonl")):
        out.append(p.stem)
    return out


def messages_for_chat(session_id: str, limit: int = 20) -> list[dict]:
    """Convert stored turns to OpenAI-style messages (user/assistant/system)."""
    out = []
    for t in load_turns(session_id, limit=limit):
        role = t.get("role") or "user"
        if role not in ("user", "assistant", "system"):
            role = "user"
        out.append({"role": role, "content": t.get("content") or ""})
    return out
