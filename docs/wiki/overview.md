# Project Overview

CryoOmega ULTRA is a unified command-line tool, interactive TUI and browser-based IDE workspace for autonomous agents and skills orchestration. The `omega-gateway` engine owns computation while CLI, TUI and IDE act as clients. fileciteturn0file0L2-L2

## Goals

- Provide one coherent runtime for CLI, TUI and Web IDE.
- Keep gateway computation centralized and clients lightweight.
- Expose agents, skills and plugins through explicit interfaces.
- Keep operational state separate from source-controlled project files.
- Make local-first operation the safe default.

## Scope

### In scope

CLI, TUI, Web IDE, gateway, agents, skills, plugins, configuration, API, testing, operations, security and releases.

### Out of scope

Marketing copy, non-technical product claims and undocumented architectural assumptions.

## Repository map

```text
bin/                 CLI and gateway entry points
lib/ultra/           Core runtime modules
ide/                 Self-contained Web IDE
browser-extension/   Browser extension client/integration
examples/plugins/    Reference plugins
docs/                Technical documentation
tests/               Test suites
tools/               Evaluation and development tools
```

## Key runtime data

- `OMEGA_DATA` defaults to `~/.omega`.
- `OMEGA_ROOT` identifies the workspace/File API root.
- Skills live in `~/.agents/skills`.
- Plugins live in `$OMEGA_DATA/plugins`.
- Agent profiles live in `$OMEGA_DATA/agents.json`. fileciteturn1file0L2-L2

## Canonical links

- [Repository](https://github.com/Pierreg99/cryo-omega-ultra)
- [Issues](https://github.com/Pierreg99/cryo-omega-ultra/issues)
- [Pull Requests](https://github.com/Pierreg99/cryo-omega-ultra/pulls)
- [Actions](https://github.com/Pierreg99/cryo-omega-ultra/actions)
- [Security Policy](../../SECURITY.md)
- [Changelog](../../CHANGELOG.md)

## Planned pages

- [Goals & Non-Goals](goals.md)
- [Repository Map](repository-map.md)
- [FAQ](faq.md)
- [Glossary](glossary.md)

## How to use this page

Use this page for orientation and scope. Move to [Getting Started](getting-started/index.md) for execution or [Architecture](architecture/index.md) for implementation details.
