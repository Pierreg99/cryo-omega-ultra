"""Semantic memory + light RAG ingest (0.4.1).

Stdlib only: chunking + TF-cosine lexical retrieval.
Not vector embeddings — `backend: lexical` is explicit.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
from collections import Counter
from pathlib import Path

from . import config

_TOKEN = re.compile(r"[A-Za-z0-9_]{2,}")
_DOC_ID = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")


def _semantic_dir() -> Path:
    d = config.MEMORY_DIR / "semantic"
    d.mkdir(parents=True, exist_ok=True)
    (d / "chunks").mkdir(exist_ok=True)
    return d


def _docs_index() -> Path:
    return _semantic_dir() / "docs.jsonl"


def ensure_layout() -> None:
    _semantic_dir()
    readme = config.MEMORY_DIR / "README.md"
    text = (
        "# Omega memory namespaces\n\n"
        "- `working/` — session turns (0.4)\n"
        "- `semantic/` — document chunks + lexical RAG (0.4.1)\n"
        "- `episodic/`, `procedural/`, `user_project/` — reserved\n"
    )
    readme.write_text(text, encoding="utf-8")


def _tok(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN.findall(text or "")]


def chunk_text(text: str, size: int = 500, overlap: int = 80) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    # prefer paragraph boundaries
    parts = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    buf = ""
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(buf) + len(part) + 1 <= size:
            buf = f"{buf}\n\n{part}".strip()
        else:
            if buf:
                chunks.append(buf)
            if len(part) <= size:
                buf = part
            else:
                i = 0
                while i < len(part):
                    chunks.append(part[i : i + size])
                    i += max(1, size - overlap)
                buf = ""
    if buf:
        chunks.append(buf)
    return chunks


def _safe_doc_id(doc_id: str) -> str:
    doc_id = (doc_id or "").strip()
    if not _DOC_ID.match(doc_id):
        raise ValueError("doc_id must be 1–128 chars of [A-Za-z0-9_.:-]")
    return doc_id


def ingest(
    text: str,
    *,
    doc_id: str | None = None,
    source: str = "api",
    title: str = "",
    meta: dict | None = None,
) -> dict:
    """Ingest raw text into semantic store. Returns doc summary."""
    ensure_layout()
    body = (text or "").strip()
    if not body:
        raise ValueError("text required")
    digest = hashlib.sha256(body.encode()).hexdigest()[:16]
    doc_id = _safe_doc_id(doc_id or f"doc-{digest}")
    chunks = chunk_text(body)
    chunk_dir = _semantic_dir() / "chunks"
    # replace existing chunks for doc
    for old in chunk_dir.glob(f"{doc_id}__*.json"):
        old.unlink()
    records = []
    for i, ch in enumerate(chunks):
        rec = {
            "id": f"{doc_id}__{i:04d}",
            "doc_id": doc_id,
            "ord": i,
            "text": ch,
            "tokens": _tok(ch),
            "tf": dict(Counter(_tok(ch))),
        }
        (chunk_dir / f"{rec['id']}.json").write_text(
            json.dumps(rec, ensure_ascii=False), encoding="utf-8"
        )
        records.append(rec["id"])
    doc = {
        "doc_id": doc_id,
        "title": title or doc_id,
        "source": source,
        "sha256_16": digest,
        "chars": len(body),
        "chunks": len(records),
        "backend": "lexical",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "meta": meta or {},
    }
    # append/replace in docs index
    rows = [d for d in list_docs() if d.get("doc_id") != doc_id]
    rows.append(doc)
    _docs_index().write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
        encoding="utf-8",
    )
    return doc


def ingest_file(path: Path, *, doc_id: str | None = None, source: str = "file") -> dict:
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    return ingest(text, doc_id=doc_id or path.stem, source=source, title=path.name)


def list_docs() -> list[dict]:
    ensure_layout()
    idx = _docs_index()
    if not idx.exists():
        return []
    out = []
    for line in idx.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def _load_chunks() -> list[dict]:
    chunk_dir = _semantic_dir() / "chunks"
    rows = []
    for p in sorted(chunk_dir.glob("*.json")):
        try:
            rows.append(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
    return rows


def _cosine(a: Counter, b: Counter, na_val: float | None = None) -> float:
    if not a or not b:
        return 0.0

    # ⚡ Bolt: Optimize dot product by only iterating over intersection
    dot = sum(a[k] * b[k] for k in a if k in b)
    if dot == 0:
        return 0.0

    na = na_val if na_val is not None else math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))

    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def search(query: str, *, limit: int = 5, doc_id: str | None = None) -> list[dict]:
    """Lexical TF-cosine retrieval over ingested chunks."""
    ensure_layout()
    q = Counter(_tok(query))
    if not q:
        return []
    hits = []

    # ⚡ Bolt: Pre-compute query magnitude outside the loop
    q_mag = math.sqrt(sum(v * v for v in q.values()))

    for ch in _load_chunks():
        if doc_id and ch.get("doc_id") != doc_id:
            continue
        tf = Counter(ch.get("tf") or ch.get("tokens") or [])
        score = _cosine(q, tf, na_val=q_mag)
        if score <= 0:
            continue
        hits.append(
            {
                "score": round(score, 4),
                "chunk_id": ch.get("id"),
                "doc_id": ch.get("doc_id"),
                "text": ch.get("text"),
                "backend": "lexical",
            }
        )
    hits.sort(key=lambda h: h["score"], reverse=True)
    return hits[: max(1, min(limit, 50))]


def delete_doc(doc_id: str) -> bool:
    doc_id = _safe_doc_id(doc_id)
    chunk_dir = _semantic_dir() / "chunks"
    removed = False
    for old in chunk_dir.glob(f"{doc_id}__*.json"):
        old.unlink()
        removed = True
    rows = [d for d in list_docs() if d.get("doc_id") != doc_id]
    _docs_index().write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
        encoding="utf-8",
    )
    return removed
