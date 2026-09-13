# Runbook — Incident Response

1. Freeze: `omega gateway stop` if abuse suspected.
2. Collect: `~/.omega/gateway.log` (JSON lines), `omega doctor`, `/api/status` metrics.
3. Secrets: rotate any `CRYOMEGA_*_KEY` that may have leaked; never paste keys into issues.
4. Plugins: `OMEGA_NO_PLUGINS=1` or disable via `omega plugin disable <name>` then restart.
5. Bind: confirm loopback; revoke `OMEGA_GATEWAY_ALLOW_REMOTE` if set.
6. Resume: restart gateway; verify `/healthz` and doctor hard checks.
