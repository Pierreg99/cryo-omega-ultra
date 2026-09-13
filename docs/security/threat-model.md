# Threat Model — CryoOmega ULTRA 0.2.x

## Assets
- LLM API keys (env)
- Local filesystem under `OMEGA_ROOT` (File API)
- Agent registry / plugins under `OMEGA_DATA` (`~/.omega`)
- Chat prompts and model outputs (ephemeral unless user persists)

## Trust boundaries
1. Operator machine ↔ Gateway (HTTP on loopback)
2. Gateway ↔ Provider HTTPS APIs
3. Gateway ↔ Plugin code (same process)
4. Browser IDE ↔ Gateway (same origin when served by gateway)

## Threats and mitigations (IST)
| ID | Threat | Severity | Mitigation IST | Gap |
|----|--------|----------|----------------|-----|
| T1 | Remote File API exposure | High | Loopback default + `OMEGA_GATEWAY_ALLOW_REMOTE` gate | Auth still absent if remote |
| T2 | Secret leakage to git/logs | High | Env-only keys; `.gitignore` `.env` | Log redaction incomplete |
| T3 | Malicious plugin | High | Allowlist / ALLOW_REMOTE; remote installs disabled; disable list | Signatures / subprocess sandbox later |
| T4 | Path traversal via `/api/file` | Med | `_safe_root` resolve+relative_to | Keep regression tests |
| T5 | Prompt injection via skills/docs | Med | Operator-trusted content | No sanitizer yet |
| T6 | SSRF via provider URL env | Low | Operator-controlled env URLs | Document risk |

## Out of scope (0.2.x)
Multi-tenant auth, cloud deployment hardening, Memory/RAG data isolation (planned 0.4+).
