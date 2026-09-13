# Runbook: Restart Gateway

- **Owner:** Operations / Maintainer
- **Severity:** P2-P4 depending on impact
- **Last reviewed:** 2026-09-14

## Purpose

Restart the local gateway cleanly and verify that clients can reconnect.

## Preconditions

- Repository checkout is available.
- No active migration is running.

## Procedure

### 1. Inspect status

```bash
./bin/omega gateway status
```

### 2. Restart

```bash
./bin/omega gateway restart
```

### 3. Verify

```bash
./bin/omega gateway status
./bin/omega doctor
```

### 4. Inspect logs when needed

```bash
./bin/omega gateway log
```

## Rollback

If restart does not restore service, stop the gateway and use the incident-response procedure rather than repeatedly restarting it.

## Success criteria

- Gateway reports reachable/healthy.
- `omega doctor` does not report a hard gateway failure.
- TUI or Web IDE can reconnect.

## Evidence

Record relevant timestamps and gateway log output in the incident or issue.