# CryoOmega ULTRA — Project Profile

## Identity

- Project: CryoOmega ULTRA
- Repository: `Pierreg99/cryo-omega-ultra`
- Default branch: `main`
- Primary language: Python
- Package version line: `0.4.0`
- License: MIT
- Primary surfaces: CLI, TUI, Web IDE, gateway

## Technical scope

CryoOmega ULTRA provides a gateway-centered runtime and client surfaces for agents, skills and plugins. The repository also includes browser-extension sources, evaluation tooling, operational documentation and a Docs-as-Code wiki source.

## Repository responsibilities

| Area | Source of truth |
|---|---|
| Runtime code | `lib/ultra/`, `bin/` |
| Web IDE | `ide/` |
| Browser extension | `browser-extension/` |
| Plugins | `examples/plugins/` and plugin docs |
| Tests | `tests/` |
| Evaluation | `tools/`, `bundle/` |
| Technical docs | `docs/` |
| Wiki source | `docs/wiki/` |
| Security policy | `SECURITY.md` |
| Release history | `CHANGELOG.md` |
| License | `LICENSE` |

## Operating model

```text
CLI / TUI / Web IDE
          |
          v
    omega-gateway
          |
   +------+------+------+
   |      |      |      |
agents  skills plugins providers
```

## Evidence policy

This profile distinguishes implemented repository capabilities from future integration tracks. A capability is marked implemented only when a corresponding source, command or maintained documentation exists. A concept, roadmap item or external integration must not be presented as shipped functionality.

## Related documentation

- `docs/wiki/index.md`
- `docs/wiki/github-learning.md`
- `docs/file-types.md`
- `docs/license-and-assets.md`
