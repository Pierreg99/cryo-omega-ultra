# Documentation Governance

## Ownership

| Section | Owner |
|---|---|
| Overview | Project Maintainer |
| Getting Started | Developer Experience / Maintainer |
| Architecture | Tech Lead / Architecture Owner |
| CLI/Gateway/IDE | Component Maintainer |
| Operations | SRE / DevOps |
| Security | Security Owner |
| Plugins | Extension Maintainer |
| Development | Engineering Lead |
| Releases | Release Owner |

## Review policy

Documentation changes use the same Pull Request workflow as code. A PR must update documentation when it changes a public command/API, runtime behavior, deployment procedure, security boundary or plugin lifecycle.

## Review frequency

- Architecture: every 3 months and after architectural changes.
- Operations: every 3 months and after operational changes.
- Security: every 3 months and after security-boundary changes.
- CLI/API reference: on interface changes.
- Getting Started: on installation or command changes.
- Releases: every release.

## Quality gates

- No broken internal links.
- No unexplained placeholders in published pages.
- Examples are tested or explicitly labelled illustrative.
- No secrets or sensitive credentials in examples.
- Every runbook has an owner, preconditions, verification and rollback/escalation guidance.
- Every ADR has a status and date.

## Metrics

Track a small set of useful signals:

- broken links: target 0
- stale pages past review interval: target 0
- open documentation issues
- runbooks without owners
- ADRs without status
- documentation changes accompanying relevant code changes

## Naming

Use `kebab-case` for file and directory names. Use `NNNN-short-title.md` for ADRs, `YYYY-MM-DD-short-title.md` for incidents and `<version>.md` for release pages. Avoid spaces and special characters.

## Source-of-truth policy

Do not silently duplicate `README.md`, `SECURITY.md`, `CHANGELOG.md`, `docs/architecture.md`, `docs/configuration.md`, `docs/api.md`, `docs/operations.md`, `docs/plugin-system.md`, `docs/adr/` or `docs/runbooks/`. Link to them unless the wiki intentionally becomes the new source of truth through a reviewed migration.