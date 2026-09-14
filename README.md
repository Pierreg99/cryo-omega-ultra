# CryoOmega ULTRA

**Unified CLI, TUI and Web IDE workspace for agents, skills, plugins and the OmniLink gateway.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](pyproject.toml) [![License](https://img.shields.io/badge/license-MIT-111111.svg)](LICENSE) [![CI](https://img.shields.io/github/actions/workflow/status/Pierreg99/cryo-omega-ultra/python.yml?label=CI)](https://github.com/Pierreg99/cryo-omega-ultra/actions)

> Technical project documentation. No marketing claims. Feature status is based on the current repository state.

## At a glance

CryoOmega ULTRA combines a command-line client, interactive TUI and browser-based Web IDE around the `omega-gateway` runtime. The gateway owns computation; clients communicate with it. The repository is primarily Python, with shell/Windows integration examples and documentation-first operational guidance.

### Animated project demos

![CLI demo](assets/demos/cli-demo.gif)
![Architecture flow](assets/demos/architecture-flow.gif)
![Engineering workflow](assets/demos/workflow.gif)

The GIFs are lightweight repository-local demonstrations. They are illustrative rather than test evidence.

## Feature matrix

| Capability | Status | Primary entry point |
|---|---|---|
| CLI | Available | `./bin/omega` |
| TUI chat | Available | `./bin/omega chat` |
| Gateway | Available | `./bin/omega gateway ...` |
| Web IDE | Available | `./bin/omega ide` |
| Agent registry | Available | `./bin/omega agents ...` |
| Skills | Available | `./bin/omega skills ...` |
| Planner | Available | `./bin/omega plan ...` |
| Plugins | Available | `./bin/omega plugin ...` |
| Working memory | Available in 0.4 line | `~/.omega/memory/working` |
| SSE chat chunking | Available | `Accept: text/event-stream` |
| Structured gateway logs | Available | Gateway status/log output |
| Health endpoints | Available | `/api/health`, `/healthz` |
| Browser extension | Repository component | `browser-extension/` |
| WebMCP | Integration track / documentation | `docs/` |
| Testkube | Integration track / documentation | `docs/` |
| GeoAI | Integration track / documentation | `docs/` |

## Supported surfaces

### CLI

```bash
./bin/omega doctor
./bin/omega chat
./bin/omega ide
./bin/omega agents list
./bin/omega skills list
./bin/omega plan "inspect the gateway"
./bin/omega gateway start
./bin/omega gateway status
./bin/omega gateway log
```

### Gateway

The local default is loopback-oriented. Remote binding requires explicit configuration. See [Configuration](docs/configuration.md), [Security](SECURITY.md) and the [Threat Model](docs/security/threat-model.md).

### Web IDE

The browser IDE is served by the gateway. Use `./bin/omega ide` for the documented local entry point.

## Architecture

```text
                 +--------------------+
                 |     CLI / TUI       |
                 +----------+---------+
                            |
                 +----------v---------+
                 |    omega-gateway    |
                 | REST + static IDE   |
                 +----+----+----+-----+
                      |    |    |
                    agents skills plugins
                      |    |    |
                 +----v----v----v-----+
                 | providers / runtime |
                 +---------------------+
```

Repository layout:

```text
bin/                    CLI and gateway entrypoints
lib/ultra/              Core package
ide/                    Browser IDE
browser-extension/      Extension sources and packaging
examples/               Reference integrations and plugins
tests/                  Automated tests
tools/                  Evaluation and maintenance utilities
docs/                   Technical documentation and wiki source
assets/                 Local project graphics and identity
.github/workflows/      GitHub Actions
```

## Installation

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
./bin/omega doctor
```

The package metadata currently declares Python `>=3.9` and MIT licensing. fileciteturn36file10

## Development

```bash
pytest -q
./bin/omega doctor
```

See:

- [Contributing](CONTRIBUTING.md)
- [Development](docs/development.md)
- [Testing](docs/testing.md)
- [GitHub learning roadmap](docs/wiki/github-learning.md)
- [Project profile](docs/project-profile.md)

## Documentation map

| Need | Document |
|---|---|
| First run | `docs/wiki/getting-started/` |
| Concepts | `docs/wiki/architecture/` |
| CLI/API/config | `docs/wiki/cli-gateway-ide/` |
| Operations | `docs/wiki/operations/` |
| Security | `docs/wiki/security/` and `SECURITY.md` |
| Plugins | `docs/wiki/plugins/` |
| Releases | `docs/wiki/releases/` and `CHANGELOG.md` |
| Governance | `docs/wiki/documentation-governance.md` |
| File-type guide | `docs/file-types.md` |
| License/assets | `docs/license-and-assets.md` |

## Version and changelog

Current package line: **0.4.1**. Release history and migration notes are maintained in [`CHANGELOG.md`](CHANGELOG.md) and `docs/wiki/releases/`.

## Security boundary

Do not publish the local gateway remotely without deliberate configuration and appropriate authentication/network controls. API keys belong in environment variables or an external secret store, never in tracked files. Plugins execute in-process and therefore require explicit trust.

## License

CryoOmega ULTRA is licensed under the MIT License. The canonical legal text is in [`LICENSE`](LICENSE). Asset attribution and documentation rules are in [`docs/license-and-assets.md`](docs/license-and-assets.md).

## Languages and file types

The runtime is Python-first. The repository also contains JavaScript/HTML/CSS for the Web IDE and extension, Markdown documentation, shell-oriented entrypoints, and reference Java/Windows integration files. See [`docs/file-types.md`](docs/file-types.md) for the complete repository convention.

## Links

- Repository: https://github.com/Pierreg99/cryo-omega-ultra
- Issues: https://github.com/Pierreg99/cryo-omega-ultra/issues
- Actions: https://github.com/Pierreg99/cryo-omega-ultra/actions
- Wiki: https://github.com/Pierreg99/cryo-omega-ultra/wiki
