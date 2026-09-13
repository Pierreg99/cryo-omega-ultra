"""omega-gateway — CryoOmega ULTRA engine service (REST + static IDE).

The gateway owns all computation. The CLI and the Web IDE are clients.
A future Node orchestrator arrives as a second engine behind the same
REST surface (advertised via the `X-Omega-Engine` response header).
"""
import functools
import http.server
import json
import os
import signal
import socketserver
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from . import __version__, agents, config, llm, observability, skills

REPO = Path(__file__).resolve().parents[2]
IDE_DIR = REPO / "ide"
ENGINE_NAME = "python-gateway"
_STARTED = time.time()
ACTIVE_PLUGINS = []  # set at boot by plugins.load_all()

try:
    from . import plugins
except ImportError:  # plugins land in P1
    plugins = None

# Plugin route registry: {(METHOD, path): handler(method, path, query, body)}.
# Checked only after the built-in API handlers.
ROUTES = {}


class _TCPServer(socketserver.ThreadingTCPServer):
    """Gateway server: per-request threads + fast port reuse after restart."""

    daemon_threads = True
    allow_reuse_address = True


class _Handler(http.server.SimpleHTTPRequestHandler):
    """Single handler for API (REST/JSON) + static IDE files."""

    server_version = f"CryoOmegaGateway/{__version__}"
    protocol_version = "HTTP/1.1"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(IDE_DIR), **kw)

    def log_message(self, *a):  # keep the CLI clean; log to THE gateway logfile
        try:
            with config.GATEWAY_LOG.open("a") as f:
                f.write(" ".join(str(x) for x in a) + "\n")
        except OSError:
            pass

    # -- helpers ---------------------------------------------------------
    def _request_id(self):
        rid = getattr(self, "_omega_rid", None)
        if rid:
            return rid
        rid = observability.new_request_id(self.headers.get("X-Request-Id"))
        self._omega_rid = rid
        return rid

    def _json(self, body, code=200):
        rid = self._request_id()
        if isinstance(body, dict) and "request_id" not in body:
            body = {**body, "request_id": rid}
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Omega-Engine", ENGINE_NAME)
        self.send_header("X-Request-Id", rid)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        observability.log_event(
            config.GATEWAY_LOG, "info",
            event="response", request_id=rid, path=getattr(self, "path", ""),
            code=code, bytes=len(data),
        )
        observability.record_request(ok=code < 400, request_id=rid)

    def _wants_sse(self):
        accept = (self.headers.get("Accept") or "").lower()
        return "text/event-stream" in accept

    def _sse(self, events, code=200):
        """Minimal SSE writer. events: iterable of (event, data_dict|str)."""
        rid = self._request_id()
        self.send_response(code)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Omega-Engine", ENGINE_NAME)
        self.send_header("X-Request-Id", rid)
        self.end_headers()
        for ev, data in events:
            if isinstance(data, dict):
                if "request_id" not in data:
                    data = {**data, "request_id": rid}
                payload = json.dumps(data, ensure_ascii=False)
            else:
                payload = str(data)
            chunk = f"event: {ev}\ndata: {payload}\n\n".encode()
            self.wfile.write(chunk)
            self.wfile.flush()
        observability.log_event(
            config.GATEWAY_LOG, "info",
            event="sse_done", request_id=rid, path=getattr(self, "path", ""),
        )
        observability.record_request(ok=True, request_id=rid)

    def _read_body(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            return {}

    def _safe_root(self, rel):
        p = (config.ROOT / rel).resolve()
        try:
            p.relative_to(config.ROOT)
        except ValueError:
            return None
        return p

    def _get_query(self, path):
        q = parse_qs(urlparse(path).query)
        return {k: v[0] for k, v in q.items()}

    # -- endpoints ---------------------------------------------------------
    def _api_status(self, query=None):
        self._json({
            "version": __version__,
            "engine": ENGINE_NAME,
            "uptime_s": int(time.time() - _STARTED),
            "root": str(config.ROOT),
            "skills": len(skills.local_skills()),
            "agents": len(agents.list_agents()),
            "providers": {p: bool(config.key_for(p)) for p in config.PROVIDERS},
            "plugins": ACTIVE_PLUGINS,
            "metrics": observability.snapshot(),
            "bind": {"host": config.GATEWAY_HOST, "port": config.GATEWAY_PORT},
        })

    def _api_tree(self, query):
        rel = unquote((query or {}).get("path", "."))
        base = self._safe_root(rel)
        if base is None or not base.is_dir():
            self._json({"error": "forbidden"}, 403)
            return
        entries = []
        try:
            for e in sorted(base.iterdir(), key=lambda x: (x.is_file(), x.name))[:400]:
                if e.name in config.BAD_ENTRIES:
                    continue
                entries.append({"name": e.name, "type": "dir" if e.is_dir() else "file",
                                "size": e.stat().st_size if e.is_file() else 0})
        except OSError:
            pass
        self._json({"path": rel, "entries": entries})

    def _api_file(self, query):
        rel = unquote((query or {}).get("path", ""))
        base = self._safe_root(rel)
        if base is None or not base.is_file() or base.stat().st_size > 400_000:
            self._json({"error": "forbidden"}, 403)
            return
        try:
            text = base.read_text(errors="replace")[:200_000]
        except (OSError, UnicodeError):
            text = "⟦binary file⟧"
        self._json({"path": str(base.relative_to(config.ROOT)), "content": text})

    def _api_skills(self, query):
        term = unquote((query or {}).get("q", ""))
        self._json(skills.search(term) if term else skills.local_skills())

    def _api_agents(self, segments, query=None):
        if len(segments) >= 4:  # /api/agents/<name>
            profile = agents.find_agent(segments[3])
            if profile is None:
                self._json({"error": "agent not found"}, 404)
                return
            self._json(profile)
            return
        self._json(agents.list_agents())

    def _api_chat(self, body):
        messages = body.get("messages")
        if not isinstance(messages, list) or not messages:
            self._json({"error": "messages required"}, 400)
            return
        agent_name = body.get("agent")
        if agent_name:
            persona = (agents.find_agent(agent_name) or {}).get("persona", "")
            if persona:
                messages = [{"role": "system", "content": persona}] + messages
        t0 = time.time()
        res = llm.chat(messages, provider=body.get("provider"),
                       model=body.get("model"))
        latency = res.latency_ms + int((time.time() - t0) * 1000)
        rid = self._request_id()
        usage = {
            "prompt_tokens": getattr(res, "prompt_tokens", 0),
            "completion_tokens": getattr(res, "completion_tokens", 0),
            "total_tokens": (
                getattr(res, "prompt_tokens", 0)
                + getattr(res, "completion_tokens", 0)
            ),
            "estimated": True,
        }
        observability.record_request(ok=True, latency_ms=latency, kind="chat",
                                     request_id=rid)
        observability.log_event(
            config.GATEWAY_LOG, "info",
            event="chat", request_id=rid, provider=res.provider,
            model=res.model, latency_ms=latency,
            prompt_tokens=usage["prompt_tokens"],
            completion_tokens=usage["completion_tokens"],
        )
        payload = {
            "provider": res.provider,
            "model": res.model,
            "text": res.text,
            "latency_ms": latency,
            "usage": usage,
        }
        if self._wants_sse():
            # Provider-native token streaming remains future work; we SSE-chunk
            # the completed reply for progressive IDE rendering.
            text = res.text or ""
            size = 48
            chunks = [text[i:i + size] for i in range(0, max(len(text), 1), size)] or [""]

            def events():
                yield ("meta", {"provider": res.provider, "model": res.model,
                                "usage": usage, "latency_ms": latency})
                for ch in chunks:
                    yield ("token", {"text": ch})
                yield ("done", payload)

            return self._sse(events())
        self._json(payload)

    def _api_plan(self, body):
        task = (body.get("task") or "").strip()
        if not task:
            self._json({"error": "task required"}, 400)
            return
        t0 = time.time()
        res = llm.complete(
            "You are cryo-omega-plan-mode. Draft a concise, staged execution plan "
            f"(steps, risks, budget) for: {task}", model=body.get("model"))
        self._json({"provider": res.provider, "model": res.model, "text": res.text,
                    "latency_ms": res.latency_ms + int((time.time() - t0) * 1000)})

    # -- routing ---------------------------------------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        segs = [unquote(s) for s in parsed.path.split("/")]
        query = self._get_query(self.path)

        if parsed.path in ("/api/status", "/api/health", "/healthz"):
            return self._api_status(query)
        if parsed.path.startswith("/api/tree"):
            return self._api_tree(query)
        if parsed.path.startswith("/api/file"):
            return self._api_file(query)
        if parsed.path.startswith("/api/skills"):
            return self._api_skills(query)
        if parsed.path.startswith("/api/agents"):
            return self._api_agents(segs, query)
        if parsed.path.startswith("/api/plugins") and plugins:
            sp_ = [unquote(s) for s in parsed.path.split("/")]
            if len(sp_) >= 5 and sp_[4] in ("enable", "disable"):
                if sp_[3] not in plugins.discover():
                    self._json({"error": "plugin not found"}, 404)
                    return
                state = plugins.set_enabled(sp_[3], sp_[4] == "enable")
                self._json({"plugin": sp_[3], "enabled": state,
                            "note": "restart gateway to apply to running routes"})
                return
            self._json({name: {"name": name, **meta}
                        for name, meta in plugins.discover().items()})
            return
        hit = ROUTES.get(("GET", parsed.path.rstrip("/")))
        if hit:
            return hit(self, "GET", parsed.path, query, {})
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        segs = [unquote(s) for s in parsed.path.split("/")]
        body = self._read_body()

        if parsed.path == "/api/chat":
            return self._api_chat(body)
        if parsed.path == "/api/plan":
            return self._api_plan(body)
        if parsed.path == "/api/agents/run":
            name = (body.get("agent") or "orchestrator").strip()
            task = (body.get("task") or "").strip()
            if not task:
                self._json({"error": "task required"}, 400)
                return
            res = agents.dispatch(task, agent=name)
            res["agent"] = (agents.find_agent(name) or {"name": name}).get("name", name)
            return self._json(res)
        if parsed.path == "/api/agents":
            name = (body.get("name") or "").strip()
            if not name:
                self._json({"error": "name required"}, 400)
                return
            tags = body.get("tags")
            profile = agents.add_agent(
                name, persona=body.get("persona"), provider=body.get("provider"),
                model=body.get("model"), enabled=body.get("enabled", True),
                tags=tags.split(",") if isinstance(tags, str) else tags)
            return self._json(profile, 201)
        if parsed.path == "/api/skills/install":
            repo = (body.get("repo") or "").strip()
            if not repo:
                self._json({"error": "repo required"}, 400)
                return
            try:
                self._json({"installed": skills.add(repo)})
            except Exception as e:
                self._json({"error": str(e)[:300]}, 400)
            return
        if parsed.path.startswith("/api/plugins/install") and plugins:
            repo = (body.get("repo") or "").strip()
            if not repo:
                self._json({"error": "repo required"}, 400)
                return
            try:
                self._json({"installed": plugins.install(repo)})
            except Exception as e:
                self._json({"error": str(e)[:300]}, 400)
            return
        if parsed.path.startswith("/api/plugins") and len(segs) >= 5:
            if segs[4] in ("enable", "disable") and plugins:
                if segs[3] not in plugins.discover():
                    self._json({"error": "plugin not found"}, 404)
                    return
                state = plugins.set_enabled(segs[3], segs[4] == "enable")
                self._json({"plugin": segs[3], "enabled": state,
                            "note": "restart gateway to apply to running routes"})
                return
        hit = ROUTES.get(("POST", parsed.path.rstrip("/")))
        if hit:
            return hit(self, "POST", parsed.path, None, body)
        self._json({"error": "not found"}, 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        segs = [unquote(s) for s in parsed.path.split("/")]
        if parsed.path.startswith("/api/agents/") and len(segs) >= 4:
            removed = agents.remove_agent(segs[3])
            self._json({"removed": removed}, 200 if removed else 404)
            return
        if parsed.path.startswith("/api/plugins/") and len(segs) >= 4 and plugins:
            removed = plugins.remove(segs[3])
            self._json({"removed": removed}, 200 if removed else 404)
            return
        hit = ROUTES.get(("DELETE", parsed.path.rstrip("/")))
        if hit:
            return hit(self, "DELETE", parsed.path, None, {})
        self._json({"error": "not found"}, 404)


def serve(port=None, host=None):
    """Run the gateway in the foreground."""
    cfg = config.load()
    port = port or cfg.get("port", config.GATEWAY_PORT)
    try:
        host = config.gateway_host(host)
    except RuntimeError as exc:
        print(f"✘ {exc}", flush=True)
        return 2
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        config.GATEWAY_PID.write_text(str(os.getpid()))
    except OSError:
        pass
    handler = functools.partial(_Handler)
    with _TCPServer((host, port), handler) as httpd:
        print(f"⟦CRYOMEGA ULTRA GATEWAY⟧ {ENGINE_NAME} v{__version__}  "
              f"http://{host}:{port}", flush=True)
        if plugins:
            loaded = plugins.load_all()
            ACTIVE_PLUGINS[:] = loaded
            print(f"  plugins: {loaded if loaded else 'none enabled'}", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped", flush=True)
    return 0


def ensure_running(timeout=8.0):
    """Spawn the gateway in the background if it is not reachable."""
    if _up():
        return True
    exe = sys.executable or "python3"
    script = str(REPO / "bin" / "omega-gateway")
    try:
        log = open(config.GATEWAY_LOG, "a")
    except OSError:
        log = open(os.devnull, "a")
    try:
        subprocess.Popen([exe, script], stdout=log, stderr=log,
                         start_new_session=True)
    except OSError:
        return _up()
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _up():
            return True
        time.sleep(0.25)
    return _up()


def _up():
    from . import client
    return client.is_up()


def stop():
    """Stop a background gateway (by pid file)."""
    try:
        pid = int(config.GATEWAY_PID.read_text().strip())
    except (OSError, ValueError):
        return False
    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def main(argv=None):
    """`omega-gateway [--port N] [--host H]` — foreground engine."""
    import argparse as _a
    p = _a.ArgumentParser(prog="omega-gateway", description="CryoOmega ULTRA engine")
    p.add_argument("--port", type=int, default=None)
    p.add_argument("--host", default=None)
    a = p.parse_args(argv)
    return serve(port=a.port, host=a.host)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from ultra.gateway import main as _main
    sys.exit(_main())