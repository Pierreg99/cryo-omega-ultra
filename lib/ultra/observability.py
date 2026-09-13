"""Structured logging + lightweight request metrics (stdlib only)."""
from __future__ import annotations

import json
import re
import threading
import time
import uuid
from pathlib import Path

_lock = threading.Lock()
_metrics = {
    "requests": 0,
    "errors": 0,
    "chat_calls": 0,
    "last_latency_ms": 0,
    "last_request_id": "",
}

_BEARER_RE = re.compile(r"(?i)(bearer)\s+\S+")
_KV_RE = re.compile(
    r"(?i)(authorization|api[_-]?key|cryomega_[a-z]+_key)\s*[:=]\s*\S+"
)


def new_request_id(incoming: str | None = None) -> str:
    if incoming and incoming.strip():
        return incoming.strip()[:64]
    return uuid.uuid4().hex[:16]


def redact(text: str) -> str:
    if not text:
        return text
    text = _BEARER_RE.sub(r"\1 [REDACTED]", text)
    return _KV_RE.sub(r"\1=[REDACTED]", text)


def log_event(log_path: Path, level: str, **fields) -> None:
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "level": level}
    row.update(fields)
    line = redact(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with _lock:
            with log_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
    except OSError:
        pass


def record_request(*, ok: bool, latency_ms: int = 0, kind: str = "http",
                   request_id: str = "") -> None:
    with _lock:
        _metrics["requests"] += 1
        if not ok:
            _metrics["errors"] += 1
        if kind == "chat":
            _metrics["chat_calls"] += 1
        if latency_ms:
            _metrics["last_latency_ms"] = int(latency_ms)
        if request_id:
            _metrics["last_request_id"] = request_id


def snapshot() -> dict:
    with _lock:
        return dict(_metrics)
