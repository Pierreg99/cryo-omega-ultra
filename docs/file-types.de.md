# Dateitypen & Integrationsleitfaden

Dieser Leitfaden beschreibt die Dateitypen von CryoOmega ULTRA und ihre Verantwortlichkeiten.

## Python (`.py`)

Python ist die Primärsprache der Runtime und der technischen Werkzeuge.

- `lib/ultra/` — Runtime
- `tools/` — Evaluation und Maintenance
- `tests/` — automatisierte Tests
- `browser-extension/scripts/` — Build-/Asset-Helfer

Änderungen an Runtime-Verhalten benötigen passende Tests und aktualisierte Dokumentation.

## Java (`.java`)

Aktuell existieren keine Java-Runtimequellen. Ein kleines Java-11-Beispiel unter `examples/integrations/java/` dient ausschließlich als Interoperabilitätsreferenz für den HTTP-Zugriff auf den lokalen Health Endpoint.

## Markdown (`.md`)

Markdown ist die Dokumentationssprache für README, Security, Changelog, ADRs, Runbooks und die Wikiquelle.

## POSIX Shell (`.sh`)

Shell-Dateien kapseln wiederholbare lokale Operator-Aufgaben. Explizite Pfade und deterministisches Verhalten sind bevorzugt.

## Windows CMD (`.cmd`)

CMD-Dateien sind dünne Windows-Wrapper. Geschäftslogik bleibt in der kanonischen CLI/Runtime.

## JavaScript / HTML / CSS

Diese Dateien bilden Web IDE und Browser Extension. Gateway-Logik sollte nicht unnötig im Browser dupliziert werden.

## Regel für neue Dateitypen

Bei einem neuen Dateityp werden Rolle, Plattform, Validierungsbefehl und Source-of-Truth in dieser Dokumentation ergänzt.
