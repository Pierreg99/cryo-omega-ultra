# File Types & Integration Guide

This guide documents the file types used by CryoOmega ULTRA and the role each type plays.

## Python (`.py`)

Primary runtime and tooling language.

Typical locations:

- `lib/ultra/` — runtime modules
- `tools/` — evaluations and maintenance utilities
- `tests/` — automated tests
- `browser-extension/scripts/` — asset/build helpers

Rules:

- Prefer small, testable modules.
- Keep configuration and secrets out of source.
- Run the repository test suite before shipping behavior changes.

## Java (`.java`)

There are currently no Java runtime sources in the repository. A minimal standard-library HTTP example is provided under `examples/integrations/java/` solely as an interoperability reference. It is not part of the Python runtime.

## Markdown (`.md`)

Documentation, ADRs, changelogs, runbooks and project guidance.

Important sources:

- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `docs/`
- `docs/wiki/`

## POSIX shell (`.sh`)

Portable command wrappers and operator examples. Prefer explicit paths, `set -eu` where appropriate, and non-interactive behavior for automation.

## Windows CMD (`.cmd`)

Windows-oriented reference wrappers. Keep them simple and delegate business logic to the canonical Python/CLI implementation.

## JavaScript / HTML / CSS

Used by the Web IDE and browser extension. Browser-side code should not duplicate gateway business logic unnecessarily.

## File-type inventory rule

When adding a new file type, update this document and identify:

1. its runtime or documentation role;
2. the supported platform;
3. the test or validation command;
4. the source-of-truth location.
