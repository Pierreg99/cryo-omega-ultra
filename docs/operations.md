# Operations

## Local engine
```bash
omega gateway start|status|stop|restart|log
omega doctor
```

Data: `~/.omega/` (`agents.json`, `plugins/`, `gateway.pid`, `gateway.log`).

## Safety
Do not expose the gateway on a public interface without auth (none in 0.2.x).
Use loopback; remote bind needs `OMEGA_GATEWAY_ALLOW_REMOTE=1`.

## Backup
Copy `OMEGA_DATA` (default `~/.omega`) and optional `~/.agents/skills`.
