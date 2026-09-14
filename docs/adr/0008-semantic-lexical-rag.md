# ADR 0008 — Semantic lexical RAG

## Problem / Kontext
Semantic namespace was empty; users need doc ingest + retrieval without paying for embedding APIs.

## Entscheidung
Stdlib chunking + TF-cosine lexical search under `$OMEGA_DATA/memory/semantic/`. Explicit `backend: lexical`. No embedding model claimed.

## Alternativen
- External embeddings — deferred; optional later behind same API.
- SQLite FTS — possible follow-up; JSON chunks keep zero deps.

## Konsequenzen
Good for keyword/overlap queries; weak for paraphrase. API stable if backend upgrades later.

## Akzeptanz
Ingest + search tests; docs state lexical clearly.
