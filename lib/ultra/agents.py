"""Agent dispatch — bridges to the Cryo Omega orchestrator pipeline."""
import json
import shutil
import subprocess
from pathlib import Path

from . import config

ORCH = config.ROOT / "agents" / "orchestrator" / "pipeline.js"


def node_available():
    return shutil.which("node") is not None


def dispatch(task, agent=None):
    """Run a task through the orchestrator pipeline when node is available,
    otherwise produce a structured dispatch plan (SafeMode level respected)."""
    cfg = config.load()
    if node_available() and ORCH.exists():
        try:
            r = subprocess.run(
                ["node", str(ORCH), "dispatch", task],
                capture_output=True, text=True, timeout=300, cwd=str(config.ROOT),
            )
            if r.returncode == 0 and r.stdout.strip():
                return {"engine": "pipeline.js", "output": r.stdout.strip()[:4000]}
        except (subprocess.TimeoutExpired, OSError):
            pass
    plan = {
        "engine": "ultra-fallback",
        "task": task,
        "agent": agent or "A021-cryo-orchestrator",
        "safemode_level": cfg.get("safemode_level", 2),
        "steps": [
            "analyze intent",
            "route to specialist (S1-S8 spectrum)",
            "execute with SafeMode guard",
            "A22 QA verify",
            "return CycleReport",
        ],
        "registry": str(config.ROOT / "agents" / "registry.json"),
    }
    return {"engine": "ultra-fallback", "output": json.dumps(plan, indent=2)}
