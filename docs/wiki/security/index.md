# Security & Threat Model

CryoOmega ULTRA is local-first. The gateway defaults to loopback, provider keys are environment-only, and the current File API has no authentication. Plugins are loaded in-process and therefore must be treated as trusted code until stronger trust controls exist. fileciteturn3file0L2-L2

## Security baseline

- Gateway bind defaults to `127.0.0.1`.
- Remote binding requires explicit `OMEGA_GATEWAY_ALLOW_REMOTE=1`.
- Never commit or persist `CRYOMEGA_*_KEY` values.
- Review third-party plugins before enabling them.
- Do not expose unauthenticated File API endpoints to untrusted networks.

## Pages

- [Threat Model](threat-model.md)
- [Trust Boundaries](trust-boundaries.md)
- [Secrets Management](secrets.md)
- [Remote Gateway Security](remote-gateway.md)
- [Plugin Trust](plugin-trust.md)
- [Security Checklist](checklist.md)

## Source documents

- [Security Policy](../../SECURITY.md)
- [Configuration](../../configuration.md)

## How to use this page

Use this index before making changes to network exposure, credentials, file access, plugin loading or other trust boundaries.