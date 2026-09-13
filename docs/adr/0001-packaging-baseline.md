# ADR 0001 — Packaging baseline

## Problem / Kontext
Checkout + Termux-Shebang + `sys.path` Hack; kein `pyproject.toml` → nicht reproduzierbar.

## Entscheidung
`pyproject.toml` (setuptools, package in `lib/ultra`), portable `#!/usr/bin/env python3`, `.env.example` für Env-Vars. Runtime bleibt stdlib-only.

## Alternativen
- Nur `requirements.txt` — unzureichend für Package-Layout.
- Poetry/PDM — zu schwer für stdlib-CLI.

## Konsequenzen
`pip install -e .` möglich; CI kann pytest mit `pythonpath=lib` fahren.

## Sicherheit / Datenschutz
Keine Secrets in Packaging; Keys bleiben Env-only.

## Migration / Rollback
Neue Dateien additiv. Rollback = Dateien entfernen, Shebang zurück.

## Akzeptanz
`pyproject.toml` + portable Shebangs + `.env.example` vorhanden; Imports mit `PYTHONPATH=lib` grün.
