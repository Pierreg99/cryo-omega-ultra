# Runbook — Troubleshooting

| Symptom | Check |
|---------|--------|
| Doctor hard fail | python≥3.9, repo `ide/`, `OMEGA_ROOT` exists |
| Gateway unreachable | `omega gateway start`; port 8787 free |
| Refuse non-loopback | unset host or set `OMEGA_GATEWAY_ALLOW_REMOTE=1` knowingly |
| No LLM answers | keys unset → offline echo; set `CRYOMEGA_*_KEY` |
| Plugin missing routes | `omega gateway restart` after install |
