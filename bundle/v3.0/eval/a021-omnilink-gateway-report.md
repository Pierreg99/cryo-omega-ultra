# Eval Report — A021-cryo-orchestrator (OmniLink Gateway Engine)

**Spektrum**: S4 (Research/Orchestration) | **Tier**: Flagship | **Model**: minimax-m3 (+failover chain, offline echo)
**Date**: 2026-09-12 | **Bundle**: v3.0 · cryo-omega-ultra v0.2.0 OmniLink P0
**Harness**: cryo-omega-agent-eval-harness (5-dim, weighted) · sandboxed instance (port 8899, fixture root/data; live 8787 gateway untouched)

## Scores
- Happy Path:  1.00 (5/5)  weight 30% → 0.300
- Edge Cases:  1.00 (4/4)  weight 25% → 0.250
- Safety:      1.00 (3/3)  weight 20% → 0.200
- Consistency: 1.00 (3/3)  weight 15% → 0.150
- Regression:  1.00 (2/2)  weight 10% → 0.100
- **Total**: 1.000 → ✅ **SHIP**

## Verdict
✅ SHIP — gateway engine + agent registry are production-ready for P0 hand-off.

## Case detail

### Happy Path (5/5)
| Case | Result |
|---|---|
| `GET /api/status` → 200, engine `python-gateway`, version 0.2.0 | ✅ |
| `GET /api/agents` → registry seeded (orchestrator + coder) | ✅ |
| `POST /api/chat` → 200 with provider/model/text keys | ✅ |
| `POST /api/agents` (eval-agent) + `GET /api/agents/eval-agent` roundtrip, persona persisted | ✅ |
| `POST /api/plan` → 200 with text | ✅ |

### Edge Cases (4/4)
| Case | Result |
|---|---|
| chat without `messages` → 400 | ✅ |
| chat with non-list `messages` → 400 | ✅ |
| agent add without `name` → 400 | ✅ |
| `GET /api/agents/does-not-exist` → 404 | ✅ |

### Safety (3/3)
| Case | Result |
|---|---|
| `GET /api/file?path=../../etc/passwd` → 403 (traversal blocked) | ✅ |
| `GET /api/tree?path=../../../` → 403 (root escape blocked) | ✅ |
| secret-pattern scan (`ghp_…`, `github_pat_…`) across status+chat responses → clean | ✅ |

### Consistency (3/3)
| Case | Result |
|---|---|
| `/api/status` identical across 3 runs (engine/version/agents stable) | ✅ |
| chat echo deterministic across 3 runs (offline echo, temp=0) | ✅ |
| registry listing stable + sorted | ✅ |

### Regression (2/2) — v0.1.0 legacy behaviors
| Case | Result |
|---|---|
| `GET /api/skills` list behavior preserved | ✅ |
| `GET /api/tree` + `GET /api/file` browse behavior preserved | ✅ |

## Findings
- All 17 cases pass; no P0 blockers.
- `serve()` port resolution prefers `.omega.yaml`/DEFAULTS over `OMEGA_GATEWAY_PORT` env
  (env override requires explicit `--port`). Cosmetic; documented here for the P2 pass.
- Live provider path exercised only via offline echo in sandbox (no keys set) —
  failover chain logic unchanged from v0.1.0 `llm.py`.

## Recommended actions
- Proceed with P0 commit/push; P1 plugins next (loader + install + route injection).
- P2: add `OMEGA_GATEWAY_PORT` priority over `.omega.yaml` port in `serve()`.
- Keep eval suite runnable for regression on P1/P2 (`anonymizer_rescrub.py`-style
  runtime-recovery pattern reused here; eval script: `eval_omnilink.py`).