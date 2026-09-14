"""Plugin system — installable gateway extensions.

`runtime: python` plugins are loaded in-process by the engine and receive the
`register(api)` hook (add routes, read llm/agents/skills/config).
`runtime: node` is reserved for subprocess backends (the future cryo-omega
orchestrator pipeline) and is discovered but NOT executed yet.

Install origins: `owner/repo` (shallow GitHub clone) or a local directory path.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import config

MANIFEST = "plugin.json"
ENTRY = "plugin.py"


def _allowlist_file():
    return config.DATA_DIR / "plugins-allowlist.json"


def load_allowlist():
    """Remote install allowlist: exact `owner/repo` or `owner/*` globs."""
    try:
        data = json.loads(_allowlist_file().read_text())
    except (OSError, ValueError):
        return []
    if isinstance(data, dict):
        data = data.get("allow", data.get("repos", []))
    return [str(x).strip() for x in (data or []) if str(x).strip()]


def remote_install_permitted(repo: str) -> bool:
    """Remote GitHub clones require allow flag or allowlist match."""
    if os.environ.get("OMEGA_PLUGIN_ALLOW_REMOTE", "").lower() in ("1", "true", "yes"):
        return True
    repo = repo.strip().lower()
    for entry in load_allowlist():
        e = entry.lower()
        if e.endswith("/*"):
            if repo.startswith(e[:-1]):
                return True
        elif e == repo:
            return True
    return False



def _trust_file(plugin_dir: Path) -> Path:
    return Path(plugin_dir) / "trust.json"


def _trust_of(plugin_dir: Path, meta=None) -> str:
    meta = meta or {}
    try:
        data = json.loads(_trust_file(plugin_dir).read_text())
        trust = (data.get("trust") or "").lower()
        if trust in ("sandbox", "inprocess"):
            return trust
    except (OSError, ValueError):
        pass
    trust = (meta.get("trust") or "").lower()
    if trust in ("sandbox", "inprocess"):
        return trust
    return "inprocess"


def write_trust(plugin_dir: Path, trust: str, reason: str = "") -> None:
    trust = trust if trust in ("sandbox", "inprocess") else "sandbox"
    payload = {"trust": trust, "reason": reason}
    Path(plugin_dir).mkdir(parents=True, exist_ok=True)
    _trust_file(plugin_dir).write_text(json.dumps(payload, indent=2) + "\n")


def _run_sandbox_handle(plugin_dir: Path, event: dict, timeout: float = 5.0) -> dict:
    """Run plugin.handle(event) in a subprocess (stdlib sandbox)."""
    worker = (
        "import json, sys, importlib.util\n"
        "from pathlib import Path\n"
        "root = Path(sys.argv[1])\n"
        "event = json.loads(sys.stdin.read() or \"{}\")\n"
        "spec = importlib.util.spec_from_file_location(\"omega_sb_plugin\", root / \"plugin.py\")\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
        "if not hasattr(mod, \"handle\"):\n"
        "    print(json.dumps({\"error\": \"sandbox plugin missing handle(event)\", \"status\": 500}))\n"
        "    raise SystemExit(0)\n"
        "out = mod.handle(event)\n"
        "if not isinstance(out, dict):\n"
        "    out = {\"data\": out}\n"
        "print(json.dumps(out))\n"
    )
    try:
        r = subprocess.run(
            [sys.executable or "python3", "-c", worker, str(plugin_dir)],
            input=json.dumps(event),
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(plugin_dir),
            env={
                "PATH": os.environ.get("PATH", ""),
                "PYTHONPATH": "",
                "HOME": os.environ.get("HOME", ""),
            },
        )
    except subprocess.TimeoutExpired:
        return {"error": "sandbox timeout", "status": 504}
    if r.returncode != 0:
        return {"error": (r.stderr or r.stdout or "sandbox failed")[:300], "status": 500}
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return {"error": "invalid sandbox JSON", "status": 500, "raw": (r.stdout or "")[:200]}



def discover():
    """Scan PLUGINS_DIR: {name: {manifest fields + enabled/path}}."""
    out = {}
    if not config.PLUGINS_DIR.exists():
        return out
    for d in sorted(config.PLUGINS_DIR.iterdir()):
        mf = d / MANIFEST
        if not (d.is_dir() and mf.exists()):
            continue
        try:
            meta = json.loads(mf.read_text())
        except (OSError, ValueError):
            meta = {}
        trust = _trust_of(d, meta)
        out[d.name] = {
            "name": meta.get("name", d.name),
            "description": meta.get("description", ""),
            "version": meta.get("version", ""),
            "runtime": meta.get("runtime", "python"),
            "trust": trust,
            "enabled": _enabled(d.name),
            "path": str(d),
            "sandbox_routes": meta.get("sandbox_routes") or [],
        }
    return out


def _disabled_file():
    return config.DATA_DIR / "plugins-disabled.json"


def _enabled(name):
    try:
        disabled = json.loads(_disabled_file().read_text())
    except (OSError, ValueError):
        disabled = []
    return name not in disabled


def set_enabled(name, enabled):
    try:
        disabled = json.loads(_disabled_file().read_text())
    except (OSError, ValueError):
        disabled = []
    disabled = [n for n in disabled if n != name]
    if not enabled:
        disabled.append(name)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    _disabled_file().write_text(json.dumps(sorted(disabled)))
    return _enabled(name)


def load_all():
    """Import every enabled python plugin and run its register(api) hook.

    Called once by the gateway at boot. Returns the list of loaded names.
    """
    if os.environ.get("OMEGA_NO_PLUGINS", "0").lower() in ("1", "true", "yes"):
        return []
    loaded = []
    for name, meta in discover().items():
        if not meta["enabled"]:
            print(f"  ~ plugin {name}: disabled, skipping")
            continue
        if meta["runtime"] != "python":
            print(f"  ~ plugin {name}: runtime {meta['runtime']} reserved (not executed)")
            continue
        entry = Path(meta["path"]) / ENTRY
        if not entry.exists():
            print(f"  ~ plugin {name}: {ENTRY} missing, skipping")
            continue
        trust = meta.get("trust") or _trust_of(Path(meta["path"]))
        try:
            if trust == "sandbox":
                routes = meta.get("sandbox_routes") or []
                if not routes:
                    print(f"  ~ plugin {name}: sandbox requires sandbox_routes in plugin.json")
                    continue
                plugin_dir = Path(meta["path"])

                def _make_handler(pdir):
                    def handler(h, method, path, query, body):
                        ev = {
                            "method": method,
                            "path": path,
                            "query": query or {},
                            "body": body or {},
                        }
                        out = _run_sandbox_handle(pdir, ev)
                        code = int(out.pop("status", 200)) if isinstance(out, dict) else 200
                        if not isinstance(out, dict):
                            out = {"data": out}
                        out.setdefault("sandbox", True)
                        h._json(out, code)
                    return handler

                for item in routes:
                    if not isinstance(item, (list, tuple)) or len(item) < 2:
                        continue
                    method, route_path = item[0], item[1]
                    from . import gateway as _gw
                    key = (str(method).upper(), str(route_path))
                    _gw.ROUTES[key] = _make_handler(plugin_dir)
                    print(f"  + sandbox route {method.upper()} {route_path}  (plugin {name})")
                loaded.append(name)
                continue

            spec = importlib.util.spec_from_file_location(f"omega_plugin_{name}", entry)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "register"):
                mod.register(PluginAPI(name))
            else:
                print(f"  ✘ plugin {name}: no register(api) hook")
                continue
            loaded.append(name)
        except Exception as e:  # noqa: BLE001 — plugin isolation
            print(f"  ✘ plugin {name} failed to load: {e}")
    return loaded


def install(repo, target=None):
    """Install plugin(s) from `owner/repo` (clone) or a local directory path.

    Local paths always allowed. Remote GitHub clones require
    `OMEGA_PLUGIN_ALLOW_REMOTE=1` or a match in `plugins-allowlist.json`.
    Remote installs are disabled by default until `omega plugin enable`.
    """
    repo = repo.strip().removeprefix("https://github.com/").removesuffix("/").removesuffix(".git")
    if not repo:
        raise ValueError("install requires owner/repo or a local plugin directory")
    target = Path(target or config.PLUGINS_DIR)
    target.mkdir(parents=True, exist_ok=True)
    if Path(repo).is_dir():  # local fixture / in-tree plugin
        return _install_from(Path(repo), target, disable=False)
    local = Path.cwd() / repo
    if local.is_dir():
        return _install_from(local, target, disable=False)
    if "/" not in repo:
        raise ValueError("expected owner/repo or local path")
    if not remote_install_permitted(repo):
        raise PermissionError(
            f"remote plugin install refused for {repo!r}: set "
            "OMEGA_PLUGIN_ALLOW_REMOTE=1 or add owner/repo to "
            f"{_allowlist_file()} (see ADR-0004)"
        )
    tmp = Path(tempfile.mkdtemp(prefix="omega-plugin-"))
    try:
        r = subprocess.run(
            ["git", "clone", "--depth", "1", f"https://github.com/{repo}.git",
             str(tmp / "repo")],
            capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            raise RuntimeError(f"clone failed: {r.stderr.strip()[:200]}")
        return _install_from(tmp / "repo", target, disable=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _install_from(src, target, disable=False):
    manifests = sorted(src.rglob(MANIFEST))
    if not manifests:
        raise RuntimeError(f"no {MANIFEST} manifest found in {src}")
    installed = []
    for mf in manifests:
        name = mf.parent.name
        if mf.parent == src:
            name = src.name  # manifest at the clone/path root
        dest = target / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(mf.parent, dest, ignore=shutil.ignore_patterns(".git"))
        if disable:
            set_enabled(name, False)
            write_trust(dest, "sandbox", reason="remote-clone")
        installed.append(name)
    return installed


def remove(name):
    d = config.PLUGINS_DIR / name
    if d.exists():
        shutil.rmtree(d)
        return True
    return False


class PluginAPI:
    """Interface handed to `register(api)`."""

    def __init__(self, name):
        self.name = name

    def add_route(self, method, path, handler):
        """Register an HTTP route.

        handler(request_handler, method, path, query, body) — write the response
        via request_handler._json(...) etc.
        """
        from . import gateway
        key = (method.upper(), path)
        gateway.ROUTES[key] = handler
        print(f"  + route {method.upper()} {path}  (plugin {self.name})")

    @property
    def config(self):
        from . import config as c
        return c

    @property
    def llm(self):
        from . import llm
        return llm

    @property
    def skills(self):
        from . import skills
        return skills

    @property
    def agents(self):
        from . import agents
        return agents