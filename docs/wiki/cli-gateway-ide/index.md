# CLI, Gateway & IDE Reference

This section is the technical reference for the three main user-facing surfaces and the gateway they depend on.

## CLI

Primary entry point: `./bin/omega`.

Common commands:

```bash
./bin/omega doctor
./bin/omega chat
./bin/omega ide
./bin/omega plan "<task>"
./bin/omega agents list
./bin/omega skills list
./bin/omega gateway status
./bin/omega gateway start
./bin/omega gateway stop
./bin/omega gateway restart
./bin/omega gateway log
```

These command families are part of the repository's current CLI surface. fileciteturn0file0L2-L2

## Gateway

Default configuration:

| Setting | Default |
|---|---|
| Host | `127.0.0.1` |
| Port | `8787` |
| Data | `~/.omega` |

fileciteturn4file0L2-L2

## TUI

`omega chat` provides gateway-backed interactive chat and supports slash commands such as `/agent`, `/agents`, `/plan`, `/skills` and `/model`. fileciteturn0file0L2-L2

## Web IDE

The Web IDE is served from `ide/index.html` and uses the gateway API for runtime operations.

## Configuration reference

See [Configuration](../../configuration.md) for the current environment-variable source of truth.

## Planned pages

- [CLI Reference](cli-reference.md)
- [Gateway Reference](gateway-reference.md)
- [TUI Reference](tui-reference.md)
- [Web IDE Reference](web-ide-reference.md)
- [Configuration Reference](configuration-reference.md)
- [Environment Variables](environment-variables.md)

## How to use this page

Use this index to find exact interface documentation. Operational procedures belong under [Operations](../operations/index.md).