# Cryo Omega Browser Extension Bridge

Synced from `Pierreg99/Cryo-omegaTOPTIER/browser-extension`.

Purpose: expose Cryo Omega Promoter Suite + Download Manager as cross-browser WebExtension surface and connect future Gateway/IDE actions without moving packaging authority.

## Targets

Chrome, Brave, Edge, Opera, Firefox.

## Source of truth

Packaging source remains `Cryo-omegaTOPTIER/browser-extension`.
This repo contains synchronized integration source and contract docs.

## Omega integration

The extension may call an explicitly configured Omega Gateway origin only when enabled by user settings. No hard-coded credentials. No remote code execution.

## Artifacts

ZIP bundles for browser stores/developer loading. Chromium CRX is optional and requires Chromium packaging plus signing key. Firefox distribution requires Mozilla signing for normal Release/Beta installation.
