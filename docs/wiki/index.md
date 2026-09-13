# CryoOmega ULTRA Wiki

Technical documentation for CryoOmega ULTRA as Docs as Code.

CryoOmega ULTRA combines a CLI, TUI and browser-based Web IDE around the `omega-gateway` runtime. This wiki is the navigation layer over the repository's technical documentation and should not duplicate existing source-of-truth files without a reason.

## Start here

- [Project Overview](overview.md)
- [Getting Started](getting-started/index.md)
- [Architecture & Design](architecture/index.md)
- [CLI, Gateway & IDE](cli-gateway-ide/index.md)
- [Operations & Runbooks](operations/index.md)
- [Security & Threat Model](security/index.md)
- [Plugins & Extensions](plugins/index.md)
- [Development & Contribution](development/index.md)
- [Releases & Changelog](releases/index.md)

## Existing source documents

- [Repository README](../../README.md)
- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [API](../api.md)
- [Operations](../operations.md)
- [Testing](../testing.md)
- [Plugin system](../plugin-system.md)
- [Security Policy](../../SECURITY.md)
- [Changelog](../../CHANGELOG.md)
- [Extension Changelog](../../CHANGELOG_EXTENSION.md)
- [ADRs](../adr/)
- [Runbooks](../runbooks/)

## Documentation model

| Type | Question | Location |
|---|---|---|
| Quickstart | How do I get running quickly? | `getting-started/` |
| Tutorial | How do I complete a use case? | `tutorials/` |
| How-to | How do I solve a concrete task? | `how-to/` |
| Reference | What commands, APIs or settings exist? | `cli-gateway-ide/` and `reference/` |
| Concept | Why is the system designed this way? | `architecture/` |
| Runbook | What exact operational steps should I execute? | `operations/runbooks/` |
| ADR | Why was a design decision made? | `architecture/adrs/` |

## Navigation rule

Start from the task, not from the repository tree. Use Overview for orientation, Getting Started for first execution, Architecture for internals, Operations for runtime procedures, and Security for trust-boundary questions.
