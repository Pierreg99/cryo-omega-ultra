# Configuration

## Environment
See `.env.example`.

| Variable | Purpose | Default |
|----------|---------|---------|
| `OMEGA_ROOT` | File API root | repo root |
| `OMEGA_DATA` | Engine data dir | `~/.omega` |
| `OMEGA_GATEWAY_PORT` | Port | `8787` |
| `OMEGA_GATEWAY_HOST` | Bind host | `127.0.0.1` |
| `OMEGA_GATEWAY_ALLOW_REMOTE` | Allow non-loopback | unset/refuse |
| `CRYOMEGA_*_KEY` | Provider keys | empty → offline echo |
| `CRYOMEGA_PROVIDER` / `CRYOMEGA_MODEL` | Prefer provider | from `.omega.yaml` / defaults |

## Project file
`.omega.yaml` in the project root (optional) for provider/model/port defaults.
