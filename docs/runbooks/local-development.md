# Runbook — Local Development

1. `pip install -e ".[dev]"`
2. `cp .env.example .env` (optional keys)
3. `python bin/omega doctor` — soft warnings OK without keys
4. `python bin/omega gateway start` then `python bin/omega ide`
5. Troubleshoot: `omega gateway log`, check `~/.omega/gateway.log`
