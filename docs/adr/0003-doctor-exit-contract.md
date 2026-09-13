# ADR 0003 — Doctor exit contract

## Problem / Kontext
`omega doctor` meldete ✘, exitete aber 0 → CI/Scripts blind.

## Entscheidung
Hard vs Soft Checks. Hard-Fail → exit 1. Soft (providers, skills, bun, node, orchestrator, gateway) → Warnung, exit 0. `DATA_DIR` wird bei Bedarf geseedet.

## Alternativen
- Jedes ✘ = exit 1 — bricht frische Clones ohne Keys/Skills.
- Nur JSON-Report — bricht bestehende CLI-UX.

## Konsequenzen
Scripts können `omega doctor` in CI nutzen. Soft-Warnungen bleiben sichtbar (`!`).

## Sicherheit / Datenschutz
Keine Keys geloggt (nur KEY/-).

## Migration / Rollback
CLI-Verhalten ändert Exit-Code; dokumentiert in README.

## Akzeptanz
Test: hard fail → exit 1; nur soft → exit 0.
