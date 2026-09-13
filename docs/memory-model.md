# Memory model (0.4)

## Implemented
**Working memory** — session-scoped turns:

- Path: `$OMEGA_DATA/memory/working/<session_id>.jsonl`
- Provenance per turn: `source`, `confidence`, `request_id`, `ts`
- Chat: pass `session_id` in `POST /api/chat` to load prior turns and persist new ones
- API: `GET/POST/DELETE /api/memory/working`, `GET /api/memory/sessions`
- Forget: `DELETE /api/memory/working?session_id=…`

## Reserved (not implemented)
| Namespace | Path | Purpose |
|-----------|------|---------|
| Episodic | `memory/episodic/` | past runs / decisions |
| Semantic | `memory/semantic/` | facts / docs |
| Procedural | `memory/procedural/` | skills / workflows |
| User/Project | `memory/user_project/` | preferences / project knowledge |

No embeddings / RAG retrieval in 0.4.0.
