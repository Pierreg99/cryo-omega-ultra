# Architecture & Design

## Purpose

Explain how the major CryoOmega ULTRA components interact and where architectural decisions are recorded.

## System model

```text
CLI ───────┐
TUI ───────┼──→ omega-gateway ─→ providers / agents / skills / plugins
Web IDE ───┘
```

The gateway is the central runtime boundary. Client surfaces should remain thin and use stable interfaces rather than reimplementing runtime behavior.

## Major modules

- `bin/` — command entry points and operational wrappers.
- `lib/ultra/` — core application/runtime implementation.
- `ide/` — Web IDE surface.
- `browser-extension/` — browser integration and packaging.
- `tools/` — development, packaging, and maintenance tools.
- `tests/` — automated verification.
- `docs/` — technical documentation and source references.

## Data flow

1. A user initiates an action through CLI, TUI, or Web IDE.
2. The client validates basic input and calls the gateway or local runtime interface.
3. The gateway resolves configuration and execution policy.
4. Agents, skills, plugins, and providers execute within their defined boundaries.
5. Results and diagnostics flow back to the client surface.

## Agents and skills

Agents represent higher-level execution roles. Skills provide bounded reusable procedures. Persistent agent instructions describe repository or path conventions; task-specific skills should contain task-specific behavior.

## Plugin architecture

Plugins extend the runtime through a defined plugin interface. Because plugins are executable code, plugin trust and lifecycle rules belong in the security and plugin documentation.

## Design principles

- Prefer stable narrow interfaces.
- Keep clients thin and the runtime authoritative.
- Treat configuration and secrets as explicit boundaries.
- Separate operational procedures from architectural concepts.
- Record material architectural decisions as ADRs.

## Planned subpages

- [Component Map](component-map.md)
- [Data Flow](data-flow.md)
- [Agent Architecture](agent-architecture.md)
- [Skill Architecture](skill-architecture.md)
- [Plugin Architecture](plugin-architecture.md)
- [Storage](storage.md)
- [ADRs](adrs/index.md)

## How to use this page

Use this page to understand boundaries and data flow. Consult component references for implementation details and ADRs for historical design rationale.
