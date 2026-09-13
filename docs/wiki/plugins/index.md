# Plugins & Extensions

Plugins are installable extensions that can add gateway web routes and other integration behavior. The current implementation loads Python plugins in-process, so plugin installation is a trust decision. fileciteturn0file0L2-L2 fileciteturn3file0L2-L2

## Lifecycle

```text
Discover -> Review -> Install -> Enable -> Operate -> Disable/Remove
```

## Safe installation

1. Identify source and version.
2. Review code and permissions.
3. Run tests or the reference plugin validation.
4. Install into `$OMEGA_DATA/plugins`.
5. Enable explicitly.
6. Verify gateway health and logs.

## Reference

- [Plugin system](../../plugin-system.md)
- [Plugin Trust](../security/plugin-trust.md)
- [Reference Plugin](reference-plugin.md)
- [Plugin Lifecycle](lifecycle.md)
- [Plugin API](api.md)

## Planned pages

- Installation
- Compatibility
- Testing
- Troubleshooting
- Extension patterns

## How to use this page

Use it before installing or designing an extension. For security-sensitive plugin questions, follow the Security section first.