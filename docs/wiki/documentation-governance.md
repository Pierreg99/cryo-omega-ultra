# Wiki & Documentation Governance

## Purpose

This document defines how the CryoOmega ULTRA technical wiki is organized, changed, reviewed, and kept aligned with the codebase.

## Scope

The rules apply to `docs/wiki/` and to documentation changes that describe CLI, TUI, Web IDE, gateway, agents, skills, plugins, operations, security, releases, and contribution practices.

## Ownership

| Area | Owner | Review cadence |
|---|---|---|
| Overview / Goals | Project Maintainer | Quarterly |
| Getting Started | Developer Experience | Monthly after functional changes |
| Architecture | Technical Lead | Quarterly and after architecture changes |
| CLI / Gateway / IDE | Component Maintainers | Per interface change |
| Operations / Runbooks | Operations Owner | Quarterly and after incidents |
| Security | Security Owner | Quarterly and after security changes |
| Plugins / Extensions | Plugin Maintainer | Per API or lifecycle change |
| Development / Contribution | Maintainers | Quarterly |
| Releases | Release Owner | Every release |

## Contribution rules

1. Documentation changes are submitted through pull requests.
2. Behavior-changing code must update the relevant documentation in the same change whenever practical.
3. Examples that claim to run must be verified by the maintainer or automated checks.
4. URLs must be checked when a page is materially changed.
5. Secret values, personal tokens, private paths, and environment-specific credentials must never be committed.
6. Prefer linking to an existing source of truth over duplicating it.

## Review checklist

- [ ] The page answers one concrete question or task.
- [ ] Quickstart, tutorial, how-to, reference, concept, and runbook roles are not mixed.
- [ ] Commands and configuration names match the implementation.
- [ ] Examples are safe to copy.
- [ ] Internal links resolve.
- [ ] No secrets or machine-specific paths are present.
- [ ] Ownership and review cadence still match reality.

## Quality metrics

Track a small set of signals:

- number of open documentation issues
- age of the oldest documentation issue
- broken-link count
- percentage of major features with an owner and reference page
- percentage of release notes linked from the changelog
- top documentation pages by usage when analytics are available

## Source-of-truth hierarchy

```text
Implementation / tests
        ↓
API or configuration reference
        ↓
Wiki navigation and explanatory pages
        ↓
Tutorials and examples
```

When a conflict exists, verify against the implementation and tests first, then update the documentation.


## GitHub Wiki sync policy

Source of truth for wiki content is `docs/wiki/` in this repository (PR-gated). The GitHub Wiki is a **publish mirror only**.

Rules:

1. Sync direction is **repository → GitHub Wiki only**. Never edit GitHub Wiki as an authoring surface and never copy Wiki edits back into `docs/wiki/` without an explicit maintainer decision and a follow-up PR.
2. The empty GitHub Wiki editor (`…/wiki/_new`) without an approved page title and role is a **no-write** state. Do not publish freestyle pages there.
3. Default Home page for the mirror is `docs/wiki/index.md`, published as Wiki `Home` via `tools/publish_wiki_home.py`.
4. Relative links that leave `docs/wiki/` (for example `../architecture.md` or `../../README.md`) may need mirror-safe rewrites or absolute `https://github.com/Pierreg99/cryo-omega-ultra/blob/main/...` links before publish; the publish script records what it rewrote.
5. Line / version claims in mirrored pages must match package version (`pyproject.toml` / `lib/ultra/__init__.py`), currently **0.4.1**.

