# Plugin system (0.3)

Plugins live under **PluginHome** `$OMEGA_DATA/plugins/<name>/` with `plugin.json` + `plugin.py`.
Runtime `python` loads in-process and calls `register(PluginAPI)`.
Runtime `node` is reserved / not executed yet.

CLI: `omega plugin list|install|info|enable|disable|rm`.

## Trust (ADR-0004)
- **Local path** install: allowed; plugin stays enabled.
- **Remote** `owner/repo` clone: requires `OMEGA_PLUGIN_ALLOW_REMOTE=1` **or** an entry in `$OMEGA_DATA/plugins-allowlist.json` (`owner/repo` or `owner/*`). Remote installs start **disabled** until `omega plugin enable <name>`.
- Boot kill-switch: `OMEGA_NO_PLUGINS=1`.

Treat enabled plugins as trusted code execution in the gateway process.

Example: `examples/plugins/omega-hello`.

## Not SkillHome
Skills use `~/.agents/skills` (**SkillHome**) — do not merge with PluginHome.


## Trust levels (0.4.1 / ADR-0009)
| trust | Behavior |
|-------|----------|
| `inprocess` | `register(api)` in gateway process (full trust) |
| `sandbox` | `sandbox_routes` + `handle(event)` in subprocess per request |

Remote clones write `trust.json` with `sandbox`. Bundled examples may set `inprocess`.
