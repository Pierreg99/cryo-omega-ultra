# Memory model (0.4.1)

## Working (0.4)
Session JSONL under `$OMEGA_DATA/memory/working/`. See ADR-0007.

## Semantic / RAG (0.4.1)
Lexical (TF-cosine) ingest + search under `$OMEGA_DATA/memory/semantic/`.
- `POST /api/memory/semantic/ingest` `{text|path, doc_id?, title?}`
- `GET /api/memory/semantic/search?q=`
- `GET /api/memory/semantic/docs`
- `DELETE /api/memory/semantic/docs/<doc_id>`

Backend is explicitly **lexical**, not embeddings.

## Reserved
Episodic · Procedural · User/Project — directories only.
