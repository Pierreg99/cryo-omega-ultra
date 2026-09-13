# Gateway API (0.2.x)

Base: `http://127.0.0.1:8787` (default). Header `X-Omega-Engine: python-gateway`.

## GET
| Path | Purpose |
|------|---------|
| `/api/status` · `/api/health` · `/healthz` | version, engine, uptime, metrics, bind |
| `/api/skills` | list/search skills |
| `/api/agents` | list agents |
| `/api/agents/<name>` | agent info |
| `/api/plugins` | plugin map |
| `/api/tree?path=` | directory listing under `OMEGA_ROOT` |
| `/api/file?path=` | file read under `OMEGA_ROOT` |

## POST
| Path | Purpose |
|------|---------|
| `/api/chat` | chat (JSON response; SSE = P2) |
| `/api/plan` | plan brief |
| `/api/agents` | add agent |
| `/api/agents/run` | dispatch |
| `/api/skills/install` | install skill |
| `/api/plugins/install` | install plugin |

## DELETE
| Path | Purpose |
|------|---------|
| `/api/agents/<name>` | remove |
| `/api/plugins/<name>` | remove |

Static IDE is served from the same origin as the API.

## Correlation
Clients may send `X-Request-Id`; responses echo it and include `request_id` in JSON bodies.

## Chat SSE
Send `Accept: text/event-stream` to `POST /api/chat`. Events: `meta`, `token`, `done`.
This chunks the **completed** reply for progressive UI; provider-native streaming is still future work.
JSON responses include `usage: {prompt_tokens, completion_tokens, total_tokens, estimated: true}`.

## Memory (0.4 working)
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/memory/sessions` | list working sessions |
| GET | `/api/memory/working?session_id=` | load turns |
| POST | `/api/memory/working` | append turn `{session_id,role,content}` |
| DELETE | `/api/memory/working?session_id=` | forget session |

`POST /api/chat` accepts optional `session_id` to prepend prior working turns and persist the exchange.
