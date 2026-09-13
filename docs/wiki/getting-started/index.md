# Getting Started

## Purpose

Get a developer from a fresh checkout to a working CryoOmega ULTRA CLI, gateway, and Web IDE session.

## Quickstart

```bash
git clone https://github.com/Pierreg99/cryo-omega-ultra.git
cd cryo-omega-ultra
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
./bin/omega doctor
```

Use the repository's documented setup requirements as the source of truth if the packaging or environment requirements change.

## Start the CLI

```bash
./bin/omega --help
./bin/omega doctor
./bin/omega chat
```

## Start the gateway

```bash
./bin/omega gateway start
./bin/omega gateway status
./bin/omega gateway log
./bin/omega gateway stop
```

The default development gateway endpoint is controlled by the project's gateway configuration; do not expose it remotely without reviewing the security guidance.

## Start the Web IDE

```bash
./bin/omega ide
```

Use the CLI and Web IDE references for command-specific options rather than expanding this page into a complete reference manual.

## Configuration

Review [`docs/configuration.md`](../../configuration.md) and `.env.example` before adding provider configuration. Keep credentials outside source control.

## Troubleshooting

1. Run `./bin/omega doctor`.
2. Check gateway status and logs.
3. Verify the active Python environment.
4. Check configuration paths and provider settings.
5. Review the relevant runbook before changing runtime state.

## Planned subpages

- [Installation](installation.md)
- [CLI Quickstart](cli-quickstart.md)
- [TUI Quickstart](tui-quickstart.md)
- [Web IDE Quickstart](web-ide-quickstart.md)
- [Tutorials](../tutorials/index.md)
- [How-to Guides](../how-to/index.md)
- [Troubleshooting](troubleshooting.md)

## How to use this page

Use this page only for the shortest path to a working environment. Move detailed explanations, command matrices, and edge cases to dedicated reference or troubleshooting pages.
