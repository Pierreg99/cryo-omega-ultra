# ADR 0005 — Structured observability (light)

## Problem / Kontext
Gateway logs were free-text; no request correlation; no in-process metrics for chat/errors.

## Entscheidung
Stdlib JSON lines to `~/.omega/gateway.log` with `request_id`, path, code. Echo `X-Request-Id` / body `request_id`. In-memory metrics on `/api/status` (`requests`, `errors`, `chat_calls`, `last_latency_ms`). Secret-like tokens redacted. Health aliases `/api/health`, `/healthz`.

## Alternativen
- OpenTelemetry SDK — heavy dependency.
- External APM — out of local-first scope.

## Konsequenzen
Ops-light without new deps. Metrics reset on process restart (acceptable for 0.3.1).

## Sicherheit / Datenschutz
Redaction heuristic; do not log full prompts by default.

## Migration / Rollback
Additive. Rollback removes observability module + gateway hooks.

## Akzeptanz
Unit tests for redact/request_id/metrics; status includes metrics; JSON responses carry request_id.
