# Releases & Changelog

Release documentation records user-visible and operational impact without replacing the root `CHANGELOG.md` as the chronological source of truth. The repository also maintains `CHANGELOG_EXTENSION.md` for extension-specific changes. fileciteturn0file0L2-L2

## Release format

Every release should cover:

- Version and date
- Added / Changed / Fixed
- Security impact
- Breaking changes
- Migration steps
- Verification

## Example

# 0.4.0

- **Release type:** Minor
- **Status:** Example

## Added

- <feature>

## Changed

- <change>

## Fixed

- <fix>

## Security

- <security change or None>

## Breaking Changes

- <breaking change or None>

## Migration

```bash
<command/config update>
```

## Verification

- [ ] CLI smoke test
- [ ] Gateway smoke test
- [ ] TUI smoke test
- [ ] Web IDE smoke test
- [ ] Plugin regression tests
- [ ] Documentation reviewed

## Planned pages

- [Compatibility](compatibility.md)
- [Breaking Changes](breaking-changes.md)
- [Migrations](migrations/)
- [Deprecations](deprecations.md)

## How to use this page

Use this index for release navigation. Use `CHANGELOG.md` for the complete chronological project history.