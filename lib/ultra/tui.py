"""Immersive TUI chat — block-based terminal (Warp-style) with slash commands."""
import sys

from . import llm, skills, agents

HELP = """CRYOMEGA ULTRA · chat
  /help            this panel
  /model <name>    switch model (minimax-m3, claude-sonnet, gpt-4)
  /agent <task>    dispatch to Cryo orchestrator
  /skills [term]   list/search installed skills
  /plan <task>     draft a plan brief
  /exit            leave"""


def block(title, body):
    print(f"\n╭─ {title}")
    for line in body.splitlines() or [""]:
        print(f"│ {line}")
    print("╰────────────────────────")


def run():
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
            elif cmd == "skills":
                found = skills.search(arg) if arg else skills.local_skills()
                for s in found[:30]:
                    print(f"  {s['name']:<42} {s['description']}")
                print(f"  ({len(found)} skills)")
            elif cmd == "agent":
                if not arg.strip():
                    print("usage: /agent <task>")
                    continue
                block("AGENT DISPATCH", agents.dispatch(arg.strip())["output"])
            elif cmd == "plan":
                if not arg.strip():
                    print("usage: /plan <task>")
                    continue
                res = llm.complete(
                    f"Draft a concise execution plan for: {arg.strip()}", model=model)
                block("PLAN DRAFT", str(res))
                history.append({"role": "assistant", "content": str(res)})
            else:
                print(f"unknown command /{cmd} — /help")
            continue
        history.append({"role": "user", "content": line})
        if len(history) > 24:
            history = history[-24:]
        res = llm.chat(history, model=model)
        block(f"{res.provider} · {res.model} · {res.latency_ms}ms", res.text)
        history.append({"role": "assistant", "content": res.text})
