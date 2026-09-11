# Spec: CryoOmega ULTRA v0.2.0 "OmniLink" — Gateway Architecture Extension

**Date:** 2026-09-11
**Repo:** https://github.com/Pierreg99/cryo-omega-ultra
**Branch:** main
**Status:** Approved by user (brainstorm A23 SafeMode reviewed) — pending P0 implementation

## Goal

Extend cryo-omega-ultra (v0.1.0 Spectrum Prime) with four capabilities while moving to a
decoupled **gateway/sidecar** architecture:

1. **Live LLM in the Web IDE** — browser chat reaches the real provider failover chain
   (minimax → anthropic → openai, offline echo fallback) instead of the hardcoded echo.
2. **More CLI commands** — `agents`, `plugin`, `gateway`, `chat --web` surface.
3. **Plugins** — installable extensions (Python in-process now; `runtime: node`
   subprocess backends reserved for the future orchestrator), adding routes + commands.
4. **Agent registry** — named persona profiles usable from CLI and IDE.

## Architecture

A single standalone engine service, **`omega-gateway`** (own process, `127.0.0.1:8787`),
owns all computation. The CLI and the Web IDE are both *clients*. The gateway serves the
static IDE and the REST + SSE API on one port. A future Node orchestrator arrives as a
second engine behind the same REST surface (engine advertised via `X-Omega-Engine`).

```
┌────────────┬────────────┐        ┌───────────────────────────────┐
│  omega CLI │  IDE (web) │  HTTP  │   omega-gateway              │
│  (client)  │  (client)  │ ─────► │  /api/* REST + SSE            │
│            │            │        │  static: ide/index.html       │
└────────────┴────────────┘        │  engines: [python-gateway]    │
                                   │  plugins: <py | node>*        │
                                   └──────────────┬────────────────┘
                                                  │ llm.chat/stream
                                                  │ agents, skills
                                           ~/.omega/{agents.json, plugins/}
```

## File layout (delta on top of v0.1.0)

```
bin/omega-gateway            NEW  thin wrapper around `lib/ultra/gateway.py`
bin/omega                    CLI → gateway client; auto-spawns gateway when down
lib/ultra/gateway.py         NEW  engine: routes, SSE, plugin registry, agents,
                                   llm wiring, static IDE serving
lib/ultra/client.py          NEW  typed HTTP client (used by CLI + TUI + future tools)
lib/ultra/plugins.py         NEW  plugin loader/installer
lib/ultra/agents.py          registry CRUD — owned by gateway (single writer = engine)
lib/ultra/config.py          + DATA_DIR, AGENTS_JSON, PLUGINS_DIR,
                               GATEWAY_HOST, GATEWAY_PORT
lib/ultra/__init__.py        version → 0.2.0
lib/ultra/llm.py             + stream() (P2: real SSE per provider)
lib/ultra/tui.py             chat/plan/skills/agents via client
ide/index.html               rewired to gateway /api/* (same origin — no CORS)
README.md                    gateway ops + architecture
```

## User data (owned by the gateway engine)

- `~/.omega/agents.json` — agent registry profiles.
- `~/.omega/plugins/<name>/{plugin.json, plugin.py}` — installed plugins.
- Overridable via `OMEGA_DATA`; project config stays `.omega.yaml`.
- **API keys remain environment-only** (`CRYOMEGA_MINIMAX_KEY`, `CRYOMEGA_ANTHROPIC_KEY`,
  `CRYOMEGA_OPENAI_KEY`) — never persisted by the registry.

## Agent registry (`agents.py` + gateway routes)

Profile schema:
```json
{ "id": "orchestrator", "name": "orchestrator",
  "provider": null, "model": null,
  "persona": "You are the Cryo Omega orchestrator...",
  "enabled": true, "tags": ["core"], "created": "…", "updated": "…" }
```
Seeded on first engine boot (defaults written with a `.bak` snapshot of any prior file).

- `load_registry()` / `list_agents()` / `find_agent(name)` / `add_agent()` / `remove_agent()`.
- `dispatch(task, agent=None)`: resolve profile → prepend `persona` as system message →
  `llm.chat()` failover chain → `{engine, provider, model, output, latency_ms}`.
- Existing `pipeline.js` bridge stays as a hook for the `orchestrator` agent and becomes
  the natural Node-plugin entry point (P3).

## Plugin system (`plugins.py`)

- Manifests: `plugin.json` `{name, description, version, runtime}`.
- `runtime: python` (default): `plugin.py` exports `def register(api)`; `api` exposes
  `add_route(method, path, handler)` (+ accessors `config`, `llm`, `skills`, `agents`).
  Loaded in-process by the gateway.
- `runtime: node` (reserved): gateway spawns `node plugin/server.js` and proxies
  `/engine/<name>/*` to it. **This is where the Cryo Omega orchestrator pipeline lives
  later (P3), including staged plans / checkpoint-resume.**
- Install: `omega plugin install <owner/repo>` — shallow-clone pattern borrowed from
  `skills.py`; gateway runs the installer on `POST /api/plugins/install`.
- Enable/disable + `OMEGA_NO_PLUGINS=1` escape hatch (SafeMode).

## Gateway API surface (all `127.0.0.1:<GATEWAY_PORT>`, default 8787)

| Method / Path | Purpose |
|---|---|
| `GET /api/status` | version, engine, uptime, skills#, agents#, providers, plugins# |
| `GET /api/skills?q=` | skills list/search |
| `GET /api/agents` · `GET/POST/DELETE /api/agents/<name>` | registry CRUD |
| `POST /api/chat` | `{messages, agent?}` → JSON `{provider, model, text, latency_ms}`; `Accept: text/event-stream` → SSE (`meta`/`delta`/`done`) |
| `POST /api/agents/run` | `{agent, task}` → persona dispatch via `llm.chat` |
| `POST /api/plan` | LLM plan draft |
| `GET /api/plugins` · `POST /api/plugins/install` · enable/disable | plugin surface |
| `GET /api/tree` · `GET /api/file` | IDE file browser (kept; traversal-guarded) |
| `GET /` | `ide/index.html` + assets |

Headers: `X-Omega-Engine: python-gateway` (future: `node-gateway`).

## CLI behavior (`bin/omega`)

- Gateway-backed: `omega chat`, `omega plan`, `omega agent run <agent> <task>`,
  `omega agents list|info|run|add|rm`, `omega plugin list|install|info|enable|disable`.
- Gateway ops: `omega gateway status|restart|log`, `omega ide` (ensure gateway + open
  browser), `omega chat --web [--port N]` (launch IDE chat).
- Auto-spawn the gateway in the background when it is not answering (same pattern as the
  current `cmd_ide`).
- `omega doctor` — local checks + remote gateway checks; `--json` output (P2).

## IDE rewiring (`ide/index.html`)

- `send()` non-slash → `POST /api/chat` with conversation history; renders
  `{provider, model, text}` (offline echo shown when no keys — same honest UX).
- `/agent <name> <task>` → `{agent, task}` via `/api/chat` or `/api/agents/run`.
- Palette additions: agents, plugins, new chat; provider status chip.
- P2: SSE streaming renderer (incremental text).

## Sequencing

- **P0 (core):** gateway service (static + status/skills/tree/file + agents CRUD + JSON
  chat), CLI-as-client, IDE rewired. Version → 0.2.0.
- **P1 (plugins):** Python plugin loader + install/enable/disable + node-runtime proxy
  skeleton.
- **P2 (polish):** real SSE streaming (minimax/openai SSE, anthropic), streaming chat UI,
  doctor `--json`, README ops docs.
- **P3 (deferred):** Node orchestrator as gateway backend (engine swap), staged
  execution plans.

## QA validation plan (A22 — pre-handoff)

- `python3 -m py_compile` on all modules; `omega doctor` all-green incl. new checks.
- Boot gateway → curl every endpoint (`/api/status`, `/api/skills`, `/api/agents`,
  `/api/chat`, `/api/plugins`, `/api/tree`, `/api/file`).
- CLI roundtrip against a running gateway; kill gateway → CLI auto-respawns it.
- Plugin fixture installed from a local git repo; verify route + command injection (P1).
- Browser check of IDE (offline echo today; live once keys set).
- Regression: existing `chat/skills/plan/tree/file/status` behaviors preserved.

## Risk check (A23 SafeMode)

- Gateway binds `127.0.0.1` only; no CORS by default (`OMEGA_GATEWAY_CORS_ORIGIN` opt-in);
  loopback trust boundary documented.
- Plugin subprocess: spawned with cwd=plugin dir, timeout, captured output, terminated on
  gateway exit. Python plugins are explicit user installs only; `OMEGA_NO_PLUGINS=1`
  disables loading.
- Registry file atomically written with `.bak` snapshot before rewrite.
- Prompt-injection boundary: personas are trusted local config; documented in README.

## Deliverables

- `lib/ultra/gateway.py`, `lib/ultra/client.py`, `lib/ultra/plugins.py`
- Updated `bin/omega`, `lib/ultra/{config,agents,llm,__init__}.py`, `ide/index.html`,
  `README.md`
- `bin/omega-gateway`
- Version tag `v0.2.0-omnilink` (P0 completion).