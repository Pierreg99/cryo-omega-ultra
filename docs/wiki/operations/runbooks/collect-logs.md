# Runbook: Collect Gateway Logs

- **Owner:** Operations / Maintainer
- **Severity:** P2-P4

## Purpose

Collect the minimum evidence needed to diagnose gateway or client failures.

## Procedure

```bash
./bin/omega gateway status
./bin/omega gateway log
./bin/omega doctor
```

## Capture

Record:

- UTC/local timestamp and timezone
- gateway status output
- relevant log lines
- command/error that triggered the investigation
- affected component and client

## Security

Do not publish provider keys, tokens, session secrets or other credentials from logs.

## References

See [Operations](../index.md) and [Security](../../security/index.md).