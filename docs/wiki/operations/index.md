# Operations & Runbooks

This section provides concrete operational procedures for the gateway and surrounding runtime. Existing operations documentation identifies `omega gateway start|status|stop|restart|log` and `omega doctor` as the primary local controls. fileciteturn2file0L2-L2

## Runtime state

By default, runtime state is held under `~/.omega`, including agent registry, plugins, PID state and logs. fileciteturn2file0L2-L2

## Safety baseline

Keep the gateway on loopback unless remote access is explicitly required. Non-loopback binding requires `OMEGA_GATEWAY_ALLOW_REMOTE=1`, while the current File API has no authentication. fileciteturn3file0L2-L2

## Runbooks

- [Restart Gateway](runbooks/restart-gateway.md)
- [Collect Logs](runbooks/collect-logs.md)
- [Deployment](runbooks/deployment.md)
- [Backup & Restore](backup-restore.md)

## Planned pages

- [Environments](environments.md)
- [Deployment Guide](deployment.md)
- [Rollback Guide](rollback.md)
- [Monitoring](monitoring.md)
- [Incident Response](incident-response.md)
- [Incident Reports](incidents/)
- [Disaster Recovery](disaster-recovery.md)

## How to use this page

Start here for operational navigation. For an active problem, select the matching runbook and follow its verification/escalation steps.