# Contributing

1. Fork / branch from `main`.
2. `pip install -e ".[dev]"` then `ruff check lib tests && pytest -q`.
3. Prefer stdlib; justify new dependencies in the PR.
4. No secrets in commits. Follow `docs/security/pr-checklist.md`.
5. Small PRs; update CHANGELOG for user-visible changes.
6. See `docs/development.md` and `docs/runbooks/release-process.md`.
