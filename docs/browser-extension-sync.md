# Browser Extension Sync Contract

Date: 2026-09-12

`Pierreg99/Cryo-omegaTOPTIER/browser-extension` remains canonical packaging source.
`cryo-omega-ultra/browser-extension` mirrors extension source needed for ULTRA integration.

## Integration boundary

Browser extension owns browser permissions, download events, popup UX, context menus, and user-controlled promotion actions.

Omega ULTRA owns gateway computation, agents, skills, CLI/TUI, and Web IDE. Extension-to-gateway calls must use explicit user-configured origin and must not carry secrets in source.

## Release

Chrome/Brave/Edge/Opera use Chromium MV3 manifest. Firefox uses Gecko-specific manifest. Store distribution uses store ZIP/WebExtension packaging. CRX/XPI signing is release/distribution concern, not source sync.

## Validation

Check manifest version 3, local asset references, no remote code, queue state persistence, filter behavior, and package root containing `manifest.json`.
