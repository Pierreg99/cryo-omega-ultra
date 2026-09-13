# Operations & Runbooks

## Purpose

Provide repeatable procedures for starting, inspecting, deploying, and recovering CryoOmega ULTRA.

## Operational model

```text
environment → gateway → clients → agents/skills/plugins → providers
```

Every runbook should state prerequisites, expected state, commands, verification, and rollback or escalation.

## Runbook: Restart Gateway

### Preconditions

- Access to the target environment.
- Confirm whether a restart is safe for active sessions.

### Procedure

```bash
./bin/omega gateway status
./bin/omega gateway restart
./bin/omega gateway status
```

### Verification

- Status reports the expected running state.
- A smoke request from the intended client succeeds.
- Logs contain no new startup error.

## Runbook: Collect Logs

1. Run `./bin/omega gateway status`.
2. Run `./bin/omega gateway log`.
3. Capture timestamps, command output, environment identifier, and relevant error messages.
4. Remove secrets and tokens before attaching logs to an issue.

## Runbook: Deployment

1. Confirm the release candidate and intended environment.
2. Review CI and release checks.
3. Deploy using the repository's documented deployment mechanism.
4. Verify gateway health and a representative client path.
5. Record deployment version and outcome.

## Incident handling

Open an incident record when service impact, data integrity risk, security impact, or repeated failure requires coordinated investigation.

## Planned subpages

- [Environments](environments.md)
- [Deployment](deployment.md)
- [Rollback](rollback.md)
- [Monitoring](monitoring.md)
- [Backup & Restore](backup-restore.md)
- [Incident Response](incident-response.md)
- [Restart Gateway](runbooks/restart-gateway.md)
- [Collect Logs](runbooks/collect-logs.md)
- [Deployment Runbook](runbooks/deployment.md)

## How to use this page

Use a runbook when changing runtime state. Do not substitute a runbook for architectural documentation or a command reference.
