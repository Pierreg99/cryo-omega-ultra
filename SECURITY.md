# Security Policy

## Supported versions
| Version | Supported |
|---------|-----------|
| 0.2.x   | yes |
| < 0.2   | best-effort |

## Threat posture (summary)
CryoOmega ULTRA is a **local-first** engine. The gateway defaults to **loopback** (`127.0.0.1`). The File API (`/api/tree`, `/api/file`) has **no authentication**. Binding to a non-loopback address requires an explicit `OMEGA_GATEWAY_ALLOW_REMOTE=1` and is discouraged.

API keys (`CRYOMEGA_*_KEY`) are **environment-only** and must never be committed or written into `~/.omega/`.

Plugins load **in-process** (Python). Treat third-party plugin installs as trusted code until 0.3 trust controls land.

## Reporting a vulnerability
Email the maintainer via GitHub security advisories on this repository (Prefer privately reporting a vulnerability). Do not open a public issue with exploit details or secrets.

## Safe defaults checklist
- [ ] Gateway host is loopback unless remote intentionally enabled
- [ ] No secrets in git, logs, or agent registry JSON
- [ ] `.env` is gitignored; use `.env.example` as template
- [ ] Plugin installs reviewed before enable
