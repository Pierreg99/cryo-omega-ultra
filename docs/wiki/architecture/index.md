# Architecture & Design

CryoOmega ULTRA uses a gateway-centered runtime. `omega-gateway` owns computation; CLI, TUI and Web IDE are clients. The current architecture also keeps Skills, Plugins and the Agent Registry in distinct data homes. fileciteturn1file0L2-L2

## Architecture goals

- One runtime boundary for clients.
- Explicit module responsibilities.
- Separate trust boundaries for skills and plugins.
- Inspectable configuration and persistent state.
- Local-first safe defaults.

## Pages

- [Component Map](component-map.md)
- [Data Flow](data-flow.md)
- [Agent Architecture](agent-architecture.md)
- [Skill Architecture](skill-architecture.md)
- [Plugin Architecture](plugin-architecture.md)
- [Storage & Data Homes](storage.md)
- [Design Principles](design-principles.md)
- [ADR Index](adrs/index.md)

## Existing source

- [Existing architecture document](../../architecture.md)
- [Memory model](../../memory-model.md)

## How to use this page

Use this page to identify the right architectural document. Use ADRs to understand why a decision was made and component pages to understand how a subsystem works.