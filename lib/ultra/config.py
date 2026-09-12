import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("OMEGA_ROOT") or Path(__file__).resolve().parents[2])
HOME = Path.home()
DATA_DIR = Path(os.environ.get("OMEGA_DATA") or HOME / ".omega")
SKILLS_DIR = HOME / ".agents" / "skills"
AGENTS_JSON = DATA_DIR / "agents.json"
PLUGINS_DIR = DATA_DIR / "plugins"
GATEWAY_LOG = DATA_DIR / "gateway.log"
GATEWAY_PID = DATA_DIR / "gateway.pid"
OMEGA_YAML = Path(os.environ.get("OMEGA_CONFIG", ROOT / ".omega.yaml"))

GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = int(os.environ.get("OMEGA_GATEWAY_PORT", "8787"))
BAD_ENTRIES = (".git", "node_modules", "__pycache__")

DEFAULTS = {
    "provider": "minimax",
    "model": "minimax-m3",
    "port": 8787,
    "safemode_level": 2,
    "offline_echo": True,
}

PROVIDERS = {
    "minimax": {
        "base": os.environ.get("CRYOMEGA_MINIMAX_URL", "https://api.minimax.io/v1"),
        "key_env": "CRYOMEGA_MINIMAX_KEY",
        "model": "minimax-m3",
        "priority": 1,
    },
    "anthropic": {
        "base": os.environ.get("CRYOMEGA_ANTHROPIC_URL", "https://api.anthropic.com/v1"),
        "key_env": "CRYOMEGA_ANTHROPIC_KEY",
        "model": "claude-sonnet",
        "priority": 2,
    },
    "openai": {
        "base": os.environ.get("CRYOMEGA_OPENAI_URL", "https://api.openai.com/v1"),
        "key_env": "CRYOMEGA_OPENAI_KEY",
        "model": "gpt-4",
        "priority": 3,
    },
}


def parse_simple_yaml(text):
    cfg = {}
    section = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0 and line.strip().endswith(":"):
            section = line.strip()[:-1]
            cfg[section] = {}
            continue
        if ":" in line:
            key, _, val = line.strip().partition(":")
            val = val.strip().strip("'\"")
            try:
                val = json.loads(val) if val and val[0] in "[{\"'" else val
            except Exception:
                pass
            if val in ("true", "false"):
                val = val == "true"
            elif val.isdigit():
                val = int(val)
            if section and indent > 0:
                cfg[section][key] = val
            else:
                cfg[key] = val
    return cfg


def load():
    cfg = dict(DEFAULTS)
    if OMEGA_YAML.exists():
        try:
            cfg.update(parse_simple_yaml(OMEGA_YAML.read_text()))
        except Exception:
            pass
    if os.environ.get("CRYOMEGA_PROVIDER"):
        cfg["provider"] = os.environ["CRYOMEGA_PROVIDER"]
    if os.environ.get("CRYOMEGA_MODEL"):
        cfg["model"] = os.environ["CRYOMEGA_MODEL"]
    return cfg


def active_providers():
    return sorted(PROVIDERS.items(), key=lambda kv: kv[1]["priority"])


def key_for(provider):
    return os.environ.get(PROVIDERS[provider]["key_env"], "")
