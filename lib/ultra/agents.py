"""Agent registry + dispatch — persona profiles owned by the gateway engine."""
import json
import shutil
import subprocess
import time

from . import config, llm

ORCH = config.ROOT / "agents" / "orchestrator" / "pipeline.js"

DEFAULT_AGENTS = [
    {
        "id": "orchestrator",
        "name": "orchestrator",
        "provider": None,
        "model": None,
        "persona": (
            "You are the Cryo Omega orchestrator. Route tasks to specialist agents "
            "(S1-S8 spectrum), stage work into steps, respect SafeMode level, and "
            "return a CycleReport with evidence."
        ),
        "enabled": True,
        "tags": ["core"],
    },
    {
        "id": "coder",
        "name": "coder",
        "provider": None,
        "model": None,
        "persona": (
            "You are a focused coding specialist. Write clean, testable code and "
            "explain trade-offs."
        ),
        "enabled": True,
        "tags": ["specialist"],
    },
]


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def load_registry():
    """Read the agent registry from disk; seed defaults on first boot."""
    if not config.AGENTS_JSON.exists():
        return seed_registry()
    try:
        data = json.loads(config.AGENTS_JSON.read_text())
        agents = data if isinstance(data, list) else data.get("agents", [])
    except (OSError, ValueError):
        return seed_registry()
    return agents


def seed_registry():
    """Write the default profile set (with a .bak snapshot of any prior file)."""
    agents = [{**a, "created": _now(), "updated": _now()} for a in DEFAULT_AGENTS]
    save_registry(agents)
    return agents


def save_registry(agents):
    """Atomically persist the registry; keep a .bak snapshot of the previous file."""
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    if config.AGENTS_JSON.exists():
        try:
            config.AGENTS_JSON.rename(str(config.AGENTS_JSON) + ".bak")
        except OSError:
            pass
    tmp = config.AGENTS_JSON.with_suffix(".json.tmp")
    tmp.write_text(json.dumps({"agents": agents}, indent=2))
    tmp.rename(config.AGENTS_JSON)


def list_agents(enabled_only=False):
    return [a for a in load_registry() if not enabled_only or a.get("enabled", True)]


def find_agent(name):
    name = (name or "").strip()
    for a in load_registry():
        if a.get("id") == name or a.get("name") == name or a.get("id", "").startswith(name):
            return a
    return None


def add_agent(name, **kw):
    """Create or update a profile keyed by id/name. Returns the stored profile."""
    agents = load_registry()
    existing = find_agent(name)
    now = _now()
    if existing:
        existing.update({k: v for k, v in kw.items() if v is not None})
        existing["updated"] = now
        save_registry(agents)
        return existing
    row = {
        "id": str(name).strip().lower().replace(" ", "-"),
        "name": str(name).strip(),
        "provider": kw.get("provider"),
        "model": kw.get("model"),
        "persona": kw.get("persona", ""),
        "enabled": kw.get("enabled", True),
        "tags": kw.get("tags", []),
        "created": now,
        "updated": now,
    }
    agents.append(row)
    save_registry(agents)
    return row


def remove_agent(name):
    agents = load_registry()
    keep, removed = [], False
    for a in agents:
        if a.get("id") == name or a.get("name") == name:
            removed = True
        else:
            keep.append(a)
    if removed:
        save_registry(keep)
    return removed


def _run_pipeline(task):
    """Attempt the node orchestrator bridge (`pipeline.js`), if present."""
    if not (shutil.which("node") and ORCH.exists()):
        return None
    try:
        r = subprocess.run(
            ["node", str(ORCH), "dispatch", task],
            capture_output=True, text=True, timeout=300, cwd=str(config.ROOT),
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()[:4000]
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


def dispatch(task, agent="orchestrator"):
    """Dispatch a task to a registered agent persona through the LLM failover chain
    (node pipeline bridge attempted first for the orchestrator)."""
    profile = find_agent(agent) or find_agent("orchestrator")
    if profile is None:
        profile = {"name": agent, "persona": "", "provider": None, "model": None}
    if profile.get("id") == "orchestrator":
        out = _run_pipeline(task)
        if out:
            return {"engine": "pipeline.js", "provider": None, "model": None,
                    "output": out, "latency_ms": 0}
    messages = []
    if profile.get("persona"):
        messages.append({"role": "system", "content": profile["persona"]})
    messages.append({"role": "user", "content": task})
    res = llm.chat(messages, provider=profile.get("provider"), model=profile.get("model"))
    return {"engine": "ultra-gateway", "provider": res.provider, "model": res.model,
            "output": res.text, "latency_ms": res.latency_ms}
