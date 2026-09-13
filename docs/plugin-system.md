# Plugin system

Plugins live under `$OMEGA_DATA/plugins/<name>/` with `plugin.json` + `plugin.py`.
Runtime `python` loads in-process and calls `register(PluginAPI)`.
Runtime `node` is reserved / not executed in 0.2.x.

CLI: `omega plugin list|install|info|enable|disable|rm`.

**Trust:** treat installs as code execution. Remote/clone installs should be reviewed.
Allowlist / stronger isolation is planned for 0.3 (ADR-0004 candidate).

Example: `examples/plugins/omega-hello`.
