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
        out[d.name] = {
            "name": meta.get("name", d.name),
            "description": meta.get("description", ""),
            "version": meta.get("version", ""),
            "runtime": meta.get("runtime", "python"),
            "enabled": _enabled(d.name),
            "path": str(d),
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
        try:
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