# ADR 0009 — Plugin sandbox trust

## Problem / Kontext
In-process `register(api)` is full trust. Remote clones were already disabled-by-default (ADR-0004) but still become in-process when enabled.

## Entscheidung
`trust`: `inprocess` | `sandbox`. Remote installs write `trust.json=sandbox`. Sandbox plugins declare `sandbox_routes` and implement `handle(event)`; each request runs in a subprocess with stripped env and timeout.

## Alternativen
- WASM / seccomp — out of scope.
- Always refuse remote — too strict for extension workflows.

## Konsequenzen
Breaking for remote plugins that only expose `register` — must add `handle` + `sandbox_routes` or set `trust=inprocess` knowingly.

## Akzeptanz
Sandbox example plugin; unit test for trust defaults and subprocess handle.
