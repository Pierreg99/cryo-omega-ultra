<p align="center">
  <img src="assets/og.svg" alt="CRYOMEGA ULTRA — SPECTRUM PRIME v0.1.0" width="100%">
</p>

<p align="center">
  <img src="assets/mark.svg" alt="CryoOmega ULTRA mark" width="96">
</p>

<h1 align="center">CryoOmega ULTRA</h1>

<p align="center"><strong>CryoOmega ULTRA unified CLI & Web IDE (v0.1.0 Spectrum Prime)</strong></p>

A unified command-line tool, interactive TUI, and browser-based IDE workspace for Cryo Omega autonomous agents and skills orchestration.

## Features

- **TUI & Chat**: Interactive terminal interface (`omega chat`)
- **Agent Dispatch**: Execute and dispatch tasks across Cryo Omega specialist agents (`omega agent -t "<task>"`)
- **Skills Integration**: Discover, inspect, and manage Cryo Omega skills (`omega skills list`, `search`, `info`, `add`)
- **Execution Planner**: Staged execution planning powered by plan-mode (`omega plan "<task>"`)
- **System Doctor**: Diagnostics and environment verification (`omega doctor`)
- **Web IDE**: Integrated local HTTP service and browser IDE (`omega ide`)

## Structure

```
.
├── assets/             # Spectrum Prime identity (mark, OG)
├── bin/
│   └── omega           # Main executable CLI entrypoint
├── ide/
│   └── index.html      # Self-contained Web IDE interface
└── lib/
    └── ultra/          # Core package (agents, config, doctor, llm, skills, tui)
```

## Quick Start

```bash
# Add bin/ to your PATH or run directly:
./bin/omega doctor

# Start interactive chat
./bin/omega chat

# Launch Web IDE
./bin/omega ide --port 8765
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
