# Component Map

| Component | Path | Responsibility |
|---|---|---|
| CLI | `bin/omega` | User-facing commands and gateway client behavior |
| Gateway entry | `bin/omega-gateway` | Foreground engine entry point |
| Gateway engine | `lib/ultra/gateway.py` | REST service and static IDE delivery |
| HTTP client | `lib/ultra/client.py` | Typed calls used by CLI/TUI |
| Config | `lib/ultra/config.py` | Paths, provider selection and bind safety |
| LLM | `lib/ultra/llm.py` | Provider failover and offline fallback |
| Agents | `lib/ultra/agents.py` | Local agent profiles |
| Skills | `lib/ultra/skills.py` | Skills discovery and storage |
| Plugins | `lib/ultra/plugins.py` | In-process Python extensions |
| Doctor | `lib/ultra/doctor.py` | Health checks and exit contract |
| IDE | `ide/index.html` | Browser workspace |

The module split follows the existing architecture documentation. fileciteturn1file0L2-L2

## Boundaries

```text
CLI / TUI / Web IDE
        |
        v
   omega-gateway
   /    |     \
Agents Skills Plugins
        |
        v
   LLM / File API
```

## Ownership rule

Changes to a module should update its corresponding architecture/reference page when public behavior, storage, trust boundaries or operational behavior changes.

## How to use this page

Use it to find the implementation owner and the next detailed architectural document. Do not use it as a substitute for API or configuration reference.