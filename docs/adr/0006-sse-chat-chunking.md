# ADR 0006 — SSE chat chunking

## Problem / Kontext
IDE wants progressive output; provider-native streaming not wired.

## Entscheidung
If `Accept: text/event-stream`, `/api/chat` completes the model call then emits SSE `meta` / `token` / `done` events chunking the final text. JSON remains default.

## Alternativen
- Full provider streaming — deferred until per-provider stream parsers exist.
- WebSockets — unnecessary for unary chat.

## Konsequenzen
UX improves without claiming true token streaming from providers. Docs must say estimated chunking.

## Akzeptanz
Test: Accept header triggers SSE content-type path (unit/handler-level where practical).
