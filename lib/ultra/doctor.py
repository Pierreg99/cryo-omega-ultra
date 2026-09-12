"""Health check — omega doctor."""
import shutil
import sys
from pathlib import Path

from . import config, skills


def run():
    checks = []

    def check(name, ok, note=""):
        checks.append((name, ok, note))

    check("python", sys.version_info >= (3, 9), sys.version.split()[0])
    check("git", shutil.which("git") is not None)
    check("node", shutil.which("node") is not None)
    check("bun", shutil.which("bun") is not None)
    keyset = {p: bool(config.key_for(p)) for p in config.PROVIDERS}
    check("providers", any(keyset.values()),
          ", ".join(f"{p}:{'KEY' if k else '-'}" for p, k in keyset.items()))
    n_skills = len(skills.local_skills())
    check("skills", n_skills >= 10, f"{n_skills} installed")
    check("registry", _registry_ok(), str(config.AGENTS_JSON))
    check("data-dir", config.DATA_DIR.exists(), str(config.DATA_DIR))
    check("orchestrator", (config.ROOT / "agents" / "orchestrator" / "pipeline.js").exists())
    check("gateway", _gateway_ok(), f"127.0.0.1:{config.GATEWAY_PORT}")
    check("ide", (Path(__file__).parents[2] / "ide" / "index.html").exists())
    check("root", config.ROOT.exists(), str(config.ROOT))
    return checks


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
