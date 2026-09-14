# OMEGA MCP Pack Integration

CryoOmega ULTRA can consume the dedicated OMEGA-MCP-PACK as its MCP integration/distribution layer.

## Integration boundary

```text
OMEGA-MCP-PACK
   | server profiles
   | manifests
   | client configs
   v
CryoOmega ULTRA
   | gateway / CLI / IDE
   v
agents / skills / plugins / providers
```

The pack owns MCP packaging metadata and reference integrations. CryoOmega ULTRA remains the runtime and gateway implementation.

## Repository contract

- Keep MCP-specific packaging isolated from core runtime logic.
- Treat credentials and tokens as external configuration.
- Version MCP compatibility explicitly.
- Validate imported profiles before activation.
- Keep security-sensitive remote bindings opt-in.

See the dedicated `OMEGA-MCP-PACK` repository for pack artifacts.