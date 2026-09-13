# Quickstart

This is the minimum path to a working local CryoOmega ULTRA environment.

## 1. Clone

```bash
git clone https://github.com/Pierreg99/cryo-omega-ultra.git
cd cryo-omega-ultra
```

## 2. Diagnose

```bash
./bin/omega doctor
```

The doctor performs local checks and gateway reachability checks. Hard failures return exit code 1; soft warnings do not fail the command. fileciteturn0file0L2-L2

## 3. TUI

```bash
./bin/omega chat
```

## 4. Web IDE

```bash
./bin/omega ide
```

## 5. Gateway

```bash
./bin/omega gateway start
./bin/omega gateway status
./bin/omega gateway log
```

## 6. Configuration

The default gateway host is `127.0.0.1` and the default port is `8787`. Runtime data defaults to `~/.omega`. fileciteturn4file0L2-L2

Create a project-local `.omega.yaml` only when project-specific provider/model/port defaults are needed.

## 7. Security baseline

Keep the gateway on loopback. Remote binding requires explicit `OMEGA_GATEWAY_ALLOW_REMOTE=1` and is not a safe default because the current File API has no authentication. fileciteturn3file0L2-L2

## Success criteria

- `omega doctor` completes.
- Gateway status is healthy/reachable.
- TUI can open.
- Web IDE can open.
- No secrets were placed in Git or runtime JSON.

## Next

- [Architecture](../architecture/index.md)
- [CLI/Gateway/IDE Reference](../cli-gateway-ide/index.md)
- [Operations](../operations/index.md)
- [Security](../security/index.md)
