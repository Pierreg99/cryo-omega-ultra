# CryoOmega ULTRA

**CryoOmega ULTRA unified CLI & Web IDE (v0.1.0 Spectrum Prime)**

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

## License

MIT License
