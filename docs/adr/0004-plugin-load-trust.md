# ADR 0004 — Plugin load trust

## Problem / Kontext
Python-Plugins laden in-process mit vollem Zugriff auf config/llm/agents/skills und können Routes registrieren. Remote-Clone (`owner/repo`) war ungefiltert = Remote-Code-Execution als Operator.

## Entscheidung
1. Lokale Pfad-Installs bleiben erlaubt.
2. Remote-GitHub-Installs brauchen `OMEGA_PLUGIN_ALLOW_REMOTE=1` **oder** Match in `$OMEGA_DATA/plugins-allowlist.json` (`owner/repo` oder `owner/*`).
3. Remote-Installs starten **disabled**; Operator aktiviert explizit (`omega plugin enable`).
4. `OMEGA_NO_PLUGINS=1` bleibt Boot-Kill-Switch.

## Alternativen
- Immer remote verbieten — bricht legitime Extension-Workflows.
- Subprocess-Sandbox zuerst — größerer Scope; später möglich.
- Signierte Bundles — kein Infrastruktur-Fit in 0.3.

## Konsequenzen
Breaking für Scripts, die still remote clonen: Env/Allowlist setzen. Trust-Boundary dokumentiert; volle Isolation weiter offen.

## Sicherheit / Datenschutz
Reduziert versehentliche Remote-RCE. In-process Risiko bleibt für enabled Plugins.

## Migration / Rollback
Allowlist-Datei + Env additiv. Rollback: Checks entfernen (nicht empfohlen).

## Akzeptanz
- Remote ohne Flag/Allowlist → `PermissionError`
- Remote mit Flag → install OK, plugin disabled bis enable
- Local path → install OK, enabled
- Tests decken refuse/allow ab
