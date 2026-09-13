# Changelog

## [0.3.0] — unreleased
### Added
- ADR-0004 plugin load trust: remote install allowlist / `OMEGA_PLUGIN_ALLOW_REMOTE`
- Remote installs disabled until explicit enable
- Domain homes + local-vs-Mesh ID notes in architecture docs

## [0.2.2] — 2026-09-13
### Added
- SECURITY.md, threat model, PR security checklist
- docs: architecture, development, configuration, api, plugins, testing, operations, runbooks

## [0.2.1] — 2026-09-13
### Added
- Packaging baseline (`pyproject.toml`, portable shebangs, `.env.example`)
- Doctor hard/soft exit contract; DATA_DIR seed
- Gateway bind safety (`OMEGA_GATEWAY_ALLOW_REMOTE`)
- ADRs 0001–0003, MIT LICENSE, pytest + Python CI
### Fixed
- Spec/README drift (OmniLink no longer “pending P0”; SSE marked not shipped)

## [0.2.0] — OmniLink
- Gateway engine, agents, plugins, IDE live LLM path
