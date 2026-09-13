# ADR 0007 — Working memory (0.4)

## Problem / Kontext
Chat was request-scoped only; no durable short-term session context.

## Entscheidung
JSONL working memory under `$OMEGA_DATA/memory/working/<session_id>.jsonl` with provenance.
Optional `session_id` on `/api/chat` prepends prior turns and appends user/assistant after reply.
Reserved empty namespaces for episodic/semantic/procedural/user_project (no fake RAG).

## Alternativen
- SQLite first — heavier; JSONL sufficient for local-first.
- Full RAG now — deferred until embeddings strategy exists.

## Konsequenzen
Session IDs must be validated; forget deletes the file. Max 200 turns trimmed.

## Sicherheit / Datenschutz
Local disk only; no cloud sync. Operators should treat session files as sensitive.

## Akzeptanz
Unit tests for append/load/forget/validation; API routes documented.
