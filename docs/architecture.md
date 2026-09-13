# Architecture — CryoOmega ULTRA

## Overview
OmniLink (v0.2.x): a single **omega-gateway** process owns computation. CLI, TUI and Web IDE are clients.

## Components
| Component | Path | Role |
|-----------|------|------|
| CLI | `bin/omega` | Commands; auto-spawns gateway |
| Gateway entry | `bin/omega-gateway` | Foreground engine |
| Engine | `lib/ultra/gateway.py` | REST + static IDE |
| HTTP client | `lib/ultra/client.py` | Typed calls for CLI/TUI |
| Config | `lib/ultra/config.py` | Paths, providers, bind safety |
| LLM | `lib/ultra/llm.py` | Provider failover + echo |
| Agents | `lib/ultra/agents.py` | Profiles in `~/.omega/agents.json` |
| Skills | `lib/ultra/skills.py` | `~/.agents/skills` |
| Plugins | `lib/ultra/plugins.py` | In-process Python plugins |
| Doctor | `lib/ultra/doctor.py` | Health / exit contract |
| IDE | `ide/index.html` | Browser workspace |

## Data
- `OMEGA_ROOT` — repo / workspace for File API
- `OMEGA_DATA` — default `~/.omega` (agents, plugins, pid, log)
- Skills live under `~/.agents/skills` (separate home)

## ADRs
See `docs/adr/` (0001 packaging, 0002 bind safety, 0003 doctor exit).


## Data homes (do not merge)

| Home | Path | Holds |
|------|------|-------|
| `SkillHome` | `~/.agents/skills` | skills.sh-compatible skills (outside `OMEGA_DATA`) |
| `PluginHome` | `$OMEGA_DATA/plugins` (default `~/.omega/plugins`) | installable gateway plugins |
| `AgentRegistry` | `$OMEGA_DATA/agents.json` | local gateway agent profiles |

Skills and plugins stay separate: different protocols and trust boundaries (ADR-0004).

## Agent IDs

OmniLink `AgentProfile.id` values (e.g. `orchestrator`, `coder`) are **local gateway IDs**.
They are **not** equivalent to AGI-3 Mesh Spektrum IDs (`S1`…`S8`) or Mesh agent UUIDs.
No mapping table until an explicit multi-mesh bridge exists.
