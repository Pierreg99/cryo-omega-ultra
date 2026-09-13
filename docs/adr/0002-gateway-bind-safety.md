# ADR 0002 — Gateway bind safety

## Problem / Kontext
Gateway File-API (`/api/tree|/file`) ohne Auth. Non-Loopback-Bind wäre Remote-Exposure.

## Entscheidung
Default `127.0.0.1`. Non-Loopback nur mit `OMEGA_GATEWAY_ALLOW_REMOTE=1` via `config.gateway_host()`.

## Alternativen
- Immer Loopback erzwingen — bricht legitime LAN-Dev-Szenarien.
- Token-Auth zuerst — Scope 0.3+/0.4.

## Konsequenzen
Serve exit 2 bei verweigertem Bind. Remote-Betrieb bleibt opt-in + dokumentiert.

## Sicherheit / Datenschutz
Verhindert versehentliches Öffnen von File-API.

## Migration / Rollback
Env-Flag; Rollback entfernt Check.

## Akzeptanz
Unit-Test: non-loopback ohne Flag → RuntimeError; mit Flag → erlaubt.
