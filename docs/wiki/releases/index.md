# Releases & Changelog

## Purpose

Keep version history, compatibility expectations, migrations, and release verification in one navigable documentation area.

## Release sources

- [`CHANGELOG.md`](../../CHANGELOG.md) — canonical chronological changelog.
- `docs/wiki/releases/` — explanatory release notes and migration material.
- Git tags and GitHub Releases — published version identity and artifacts.

## Release workflow

```text
change → tests → security → changelog → version/tag → release → artifact verification
```

## Example release entry

# 0.5.0 — YYYY-MM-DD

## Summary
Consolidate the gateway, documentation, and development workflow improvements included in this release.

## Added

- Expanded technical wiki navigation.
- GitHub learning and repository-engineering guidance.

## Changed

- Clarified operational and security documentation boundaries.

## Fixed

- Documentation navigation inconsistencies.

## Breaking Changes

None unless explicitly listed in the final release notes.

## Migration

1. Read the release-specific migration notes.
2. Run the documented validation commands.
3. Confirm gateway and client compatibility.

## Verification

- CI status is green.
- Release artifacts are present and attributable to the release commit.
- Documentation matches the released behavior.

## Planned subpages

- [Compatibility](compatibility.md)
- [Breaking Changes](breaking-changes.md)
- [Deprecations](deprecations.md)
- [Migration Guides](migrations/index.md)
- [Version Notes](index.md)

## How to use this page

Use this section when upgrading, diagnosing version differences, or preparing a release. Do not duplicate the complete changelog; link to the canonical changelog instead.
