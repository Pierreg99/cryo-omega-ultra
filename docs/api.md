# Gateway API (0.2.x)

Base: `http://127.0.0.1:8787` (default). Header `X-Omega-Engine: python-gateway`.

## GET
| Path | Purpose |
|------|---------|
| `/api/status` | version, engine, uptime, root |
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
