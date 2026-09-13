# Threat Model

This document identifies the principal assets, entry points and trust boundaries of CryoOmega ULTRA. It is a living document and must be updated when runtime exposure or extension mechanisms change.

## Assets

- Workspace and File API contents
- Provider/API keys
- Agent registry
- Skills
- Plugin code
- Gateway runtime state
- Logs and session memory

## Attack surfaces

| Surface | Main concern |
|---|---|
| CLI | Malicious or malformed input |
| Web IDE | Browser-originated requests and user input |
| Gateway API | Network exposure and missing auth boundary |
| File API | Unauthorized file access if remotely exposed |
| Plugins | Arbitrary in-process Python execution |
| Provider integration | Credential handling and outbound requests |
| Configuration | Unsafe bind/runtime settings |

## Trust boundaries

```text
User / Browser
      |
      v
CLI / TUI / Web IDE
      |
      v
omega-gateway
  |       |       |
  v       v       v
Agents  Skills  Plugins
  |       |       |
  +-------+-------+
          |
          v
      External LLMs
```

## Current high-risk conditions

1. The File API currently has no authentication.
2. Non-loopback binding is explicitly possible through `OMEGA_GATEWAY_ALLOW_REMOTE=1`.
3. Plugins execute in-process and therefore inherit application privileges. fileciteturn3file0L2-L2

## Mitigations

- Keep gateway on loopback.
- Keep secrets outside Git and runtime JSON.
- Review plugin source before enablement.
- Add authentication before intentional remote exposure.
- Review security impact for new gateway routes.

## Residual risk

Document remaining risk explicitly in the relevant ADR or security exception when a mitigation cannot be applied immediately.

## How to use this page

Use this document as the starting point for security reviews. Update attack surfaces and mitigations whenever a new network endpoint, plugin capability, data store or secret is introduced.