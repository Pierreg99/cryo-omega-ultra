"""Immersive TUI chat — block-based terminal (Warp-style) with slash commands.

Talks to the omega-gateway engine via `client` (auto-spawns when down).
"""
import json
import sys

from . import client, config, gateway, skills

HELP = """CRYOMEGA ULTRA · chat (gateway-backed)
  /help            this panel
  /model <name>    switch model (minimax-m3, claude-sonnet, gpt-4)
  /agent <task>    dispatch to orchestrator agent
  /agents [term]   list/search agent registry
  /skills [term]   list/search installed skills
  /plan <task>     draft a plan brief
  /exit            leave"""


def block(title, body):
    print(f"\n╭─ {title}")
    for line in body.splitlines() or [""]:
        print(f"│ {line}")
    print("╰────────────────────────")


def _run():
    history = []
    model = None
    block("CRYOMEGA ULTRA · TUI", HELP)
    while True:
        try:
            line = input("\n\u001b[38;5;213mω›\u001b[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            return
        if not line:
            continue
        if line.startswith("/"):
            cmd, _, arg = line[1:].partition(" ")
            if cmd == "exit":
                print("bye")
                return
            elif cmd == "help":
                print(HELP)
            elif cmd == "model":
                model = arg.strip() or None
                print(f"model → {model or 'default (minimax-m3)'}")
            elif cmd == "agents":
                rows = client.agents_list()
                if isinstance(rows, dict):
                    print(rows.get("error", "gateway error"))
                else:
                    for a in rows:
                        if arg and arg not in a["name"] and arg not in (a.get("persona") or ""):
                            continue
                        print(f"  {a['name']:<20}{(a.get('persona') or '')[:56]}")
                    print(f"  ({len(rows)} agents)")
            elif cmd == "skills":
                found = skills.search(arg) if arg else skills.local_skills()
                for s in found[:30]:
                    print(f"  {s['name']:<42} {s['description']}")
                print(f"  ({len(found)} skills)")
            elif cmd == "agent":
                if not arg.strip():
                    print("usage: /agent <task>")
                    continue
                res = client.agent_run("orchestrator", arg.strip())
                block("AGENT DISPATCH", json.dumps(res, indent=2))
            elif cmd == "plan":
                if not arg.strip():
                    print("usage: /plan <task>")
                    continue
                res = client.plan(arg.strip())
                block("PLAN DRAFT", res.get("text") or res.get("error", ""))
                history.append({"role": "assistant", "content": res.get("text", "")})
            else:
                print(f"unknown command /{cmd} — /help")
            continue
        history.append({"role": "user", "content": line})
        if len(history) > 24:
            history = history[-24:]
        res = client.chat(history, model=model)
        if res.get("error"):
            block("GATEWAY ERROR", res["error"])
            history.pop()
            continue
        text = res.get("text", "")
        title = (f"{res.get('provider')} · {res.get('model')} · {res.get('latency_ms')}ms")
        block(title, text)
        history.append({"role": "assistant", "content": text})


def run():
    if not gateway.ensure_running():
        block("GATEWAY UNREACHABLE",
              "Could not start omega-gateway.\n"
              "Check ~/.omega/gateway.log, or run `omega gateway start`.")
        return
    _run()
