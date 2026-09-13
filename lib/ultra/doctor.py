"""Health check — omega doctor.

Hard checks fail the process exit code. Soft checks print ✘ but are warnings
only (fresh clones, optional tooling, offline LLM).
"""
import shutil
import sys
from pathlib import Path

from . import config, skills

# Soft: may fail on a fresh clone or without optional deps / keys.
SOFT = frozenset({"providers", "skills", "bun", "orchestrator", "gateway", "node"})


def run(*, seed_data=True):
    """Return list of (name, ok, note, hard). Seeds DATA_DIR when missing."""
    if seed_data:
        try:
            config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass

    checks = []

    def check(name, ok, note=""):
        hard = name not in SOFT
        checks.append((name, bool(ok), note, hard))

    check("python", sys.version_info >= (3, 9), sys.version.split()[0])
    check("git", shutil.which("git") is not None)
    check("node", shutil.which("node") is not None)
    check("bun", shutil.which("bun") is not None)
    keyset = {p: bool(config.key_for(p)) for p in config.PROVIDERS}
    check(
        "providers",
        any(keyset.values()),
        ", ".join(f"{p}:{'KEY' if k else '-'}" for p, k in keyset.items()),
    )
    n_skills = len(skills.local_skills())
    check("skills", n_skills >= 10, f"{n_skills} installed (soft if <10)")
    check("registry", _registry_ok(), str(config.AGENTS_JSON))
    check("data-dir", config.DATA_DIR.exists(), str(config.DATA_DIR))
    check(
        "orchestrator",
        (config.ROOT / "agents" / "orchestrator" / "pipeline.js").exists(),
    )
    check("gateway", _gateway_ok(), f"{config.GATEWAY_HOST}:{config.GATEWAY_PORT}")
    check("ide", (Path(__file__).parents[2] / "ide" / "index.html").exists())
    check("root", config.ROOT.exists(), str(config.ROOT))
    return checks


def hard_ok(checks=None):
    checks = checks if checks is not None else run()
    return all(ok for _n, ok, _note, hard in checks if hard)


def _registry_ok():
    """Registry parses (or does not exist yet — it self-seeds on boot)."""
    if not config.AGENTS_JSON.exists():
        return True
    try:
        import json

        data = json.loads(config.AGENTS_JSON.read_text())
        rows = data.get("agents", []) if isinstance(data, dict) else data
        return isinstance(rows, list)
    except (OSError, ValueError):
        return False


def _gateway_ok():
    from . import client

    return client.is_up()
