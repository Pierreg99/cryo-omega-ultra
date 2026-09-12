<p align="center">
  <img src="assets/og.svg" alt="CRYOMEGA ULTRA — OMNILINK v0.2.0" width="100%">
</p>

<p align="center">
  <img src="assets/mark.svg" alt="CryoOmega ULTRA mark" width="96">
</p>

<h1 align="center">CryoOmega ULTRA</h1>

<p align="center"><strong>CryoOmega ULTRA unified CLI, TUI, and Web IDE (v0.2.0 OmniLink)</strong></p>

A unified command-line tool, interactive TUI, and browser-based IDE workspace for Cryo Omega autonomous agents and skills orchestration. Computation lives in the **`omega-gateway`** engine service; the CLI and the IDE are lightweight clients.

## Features

- **Gateway engine**: `omega-gateway` service owns all computation (REST + static IDE);
  CLI and IDE are clients; data lives in `~/.omega/`
- **Live LLM in the IDE**: browser chat reaches the real provider failover chain
  (minimax → anthropic → openai, offline echo fallback) via `POST /api/chat`
- **Agent registry**: named persona profiles (`~/.omega/agents.json`);
  `omega agents list|info|run|add|rm`
- **TUI & Chat** (`omega chat`): gateway-backed, slash commands `/agent /agents /plan /skills /model`
- **Skills Integration** (`omega skills list|search|add|info`)
- **Execution Planner** (`omega plan "<task>"`)
- **Web IDE** (`omega ide` · `omega chat --web`): explorer, editor, chat, skills/agent
  drawers, Ctrl-K palette
- **System Doctor** (`omega doctor`); engine control (`omega gateway status|start|stop|restart|log`)
- **Plugins** *(P1)*: installable extensions adding CLI commands + web routes
- **SSE streaming** *(P2)*: real token streaming from the providers

## Structure

```
.
├── assets/               # Spectrum Prime identity (mark, OG)
├── bin/
│   ├── omega             # CLI entrypoint (gateway client)
│   └── omega-gateway     # Engine service (REST + static IDE)
├── ide/
│   └── index.html        # Self-contained Web IDE interface
└── lib/
    └── ultra/            # Core package (agents, client, config, doctor,
                          #   gateway, llm, skills, tui; plugins* in P1)
```

## Quick Start

```bash
# Add bin/ to your PATH or run directly:
./bin/omega doctor          # local checks + gateway reachability

# Interactive TUI chat (auto-starts the gateway in the background)
./bin/omega chat

# Launch the Web IDE
./bin/omega ide

# Run/monitor the engine directly
./bin/omega gateway start
./bin/omega gateway status
./bin/omega-gateway         # foreground engine
```

## Spectrum Prime

Identity extends the Cryo Omega Line (crystalline Ω, orbital nodes) with the IDE spectrum:

| Token | Hex |
|---|---|
| void | `#05070d` |
| cyan | `#00e5ff` |
| violet | `#7b5cff` |
| rose | `#ff5c8a` |
| gold | `#f5c56b` |

The live IDE is `ide/index.html`. Wordmark and version strings live in `assets/og.svg` (code-built) so the product name stays exact.

## License

MIT License
