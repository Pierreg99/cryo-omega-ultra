# Runtime Data Flow

## Request path

```text
User
  |
  +--> CLI
  +--> TUI
  +--> Web IDE
          |
          v
    omega-gateway
      |   |   |
      |   |   +--> Plugins
      |   +------> Skills
      +----------> Agents
          |
          +--> LLM provider failover
          +--> File/API layer
          +--> Runtime data under OMEGA_DATA
```

## Gateway responsibility

The gateway is the computation boundary. Clients should not independently reimplement agent, provider, skill or plugin execution semantics.

## Persistent data

| Data | Location | Boundary |
|---|---|---|
| Agent profiles | `$OMEGA_DATA/agents.json` | Gateway-local |
| Plugins | `$OMEGA_DATA/plugins` | Extension trust boundary |
| Skills | `~/.agents/skills` | Separate skill home |
| PID/log | `$OMEGA_DATA/` | Runtime state |

Skills and plugins deliberately remain separate because they have different protocols and trust boundaries. fileciteturn1file0L2-L2

## Failure flow

A client-side connection failure should first be diagnosed as a gateway availability problem. Provider failures are handled by the LLM/provider layer and may fall back to the configured offline behavior. The `doctor` command is the first diagnostic checkpoint. fileciteturn0file0L2-L2

## How to use this page

Use this page when tracing a request, deciding where a feature belongs, or defining an integration boundary.