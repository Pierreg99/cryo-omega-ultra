# Changelog

## [Unreleased] — documentation and repository presentation upgrade
### Added
- Bilingual project profile and file-type documentation (English/German)
- Repository-local animated GIF demonstrations for CLI, architecture and engineering workflow
- Java 11 interoperability reference example
- POSIX shell and Windows CMD smoke-check wrappers
- License and asset governance documentation
- Expanded README feature matrix, documentation map, development and security guidance

### Documentation
- README now separates shipped capabilities from integration tracks.
- Added explicit source-of-truth and file-type conventions.
- Added German companion README at `README.de.md`.

## [0.4.1] — unreleased
### Added
- Semantic lexical RAG ingest/search (ADR-0008)
- Plugin sandbox trust + subprocess `handle()` (ADR-0009)
- Example `omega-hello-sandbox`

## [0.4.0] — unreleased
### Added
- Working memory JSONL + `/api/memory/*` (ADR-0007)
- Optional `session_id` on `/api/chat` for durable short-term context
- Reserved memory namespace dirs (no RAG yet)

## [0.3.2] — 2026-09-13
### Added
- `/api/chat` optional SSE chunking when `Accept: text/event-stream` (ADR-0006)
- Estimated token usage on chat responses (`usage.estimated=true`)
- `docs/memory-model.md` (explicitly deferred), CONTRIBUTING, Dockerfile

## [0.3.1] — 2026-09-13
### Added
- Structured JSON gateway logs + `X-Request-Id` / `request_id`
- In-process metrics on status; `/api/health` + `/healthz`
- IDE a11y (skip link, aria, focus, empty chat state)
- ADR-0005 observability; incident + release runbooks; ruff CI

## [0.3.0] — 2026-09-13
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
