"""Gateway client — CLI/TUI/future tools talk to the engine over HTTP."""
import json
import urllib.error
import urllib.request

from . import config


def _base():
    return f"http://{config.GATEWAY_HOST}:{config.GATEWAY_PORT}"


def _req(method, path, body=None, timeout=300):
    url = _base() + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read() or b"{}")
        except (ValueError, OSError):
            return {"error": f"HTTP {e.code}"}
    except urllib.error.URLError:
        return {"error": "gateway unreachable"}


def is_up():
    try:
        with urllib.request.urlopen(_base() + "/api/status", timeout=1) as r:
            r.read()
        return True
    except Exception:
        return False


def status():
    return _req("GET", "/api/status")


def chat(messages, agent=None, model=None, provider=None, session_id=None, timeout=600):
    body = {"messages": messages}
    if agent:
        body["agent"] = agent
    if model:
        body["model"] = model
    if provider:
        body["provider"] = provider
    if session_id:
        body["session_id"] = session_id
    return _req("POST", "/api/chat", body, timeout)


def memory_sessions():
    return _req("GET", "/api/memory/sessions")


def memory_working(session_id, limit=50):
    return _req("GET", f"/api/memory/working?session_id={session_id}&limit={limit}")


def memory_append(session_id, content, role="user", **kw):
    body = {"session_id": session_id, "content": content, "role": role, **kw}
    return _req("POST", "/api/memory/working", body)


def memory_forget(session_id):
    return _req("DELETE", f"/api/memory/working?session_id={session_id}")


def plan(task):
    return _req("POST", "/api/plan", {"task": task})


def agents_list():
    return _req("GET", "/api/agents")


def agent_info(name):
    return _req("GET", f"/api/agents/{name}")


def agent_add(name, **kw):
    return _req("POST", "/api/agents", {"name": name, **kw})


def agent_remove(name):
    return _req("DELETE", f"/api/agents/{name}")


def agent_run(name, task):
    return _req("POST", "/api/agents/run", {"agent": name, "task": task})


def skills(q=""):
    return _req("GET", "/api/skills" + (f"?q={q}" if q else ""))


def skills_install(repo):
    return _req("POST", "/api/skills/install", {"repo": repo})


def tree(path="."):
    return _req("GET", "/api/tree?path=" + path)


def file_read(path):
    return _req("GET", "/api/file?path=" + path)


def plugins():
    return _req("GET", "/api/plugins")


def plugin_install(repo):
    return _req("POST", "/api/plugins/install", {"repo": repo})


def plugin_enable(name, enabled=True):
    return _req("GET", f"/api/plugins/{name}/{'enable' if enabled else 'disable'}")


def plugin_remove(name):
    return _req("DELETE", f"/api/plugins/{name}")

def semantic_ingest(text=None, path=None, **kw):
    body = {**kw}
    if text is not None:
        body["text"] = text
    if path is not None:
        body["path"] = path
    return _req("POST", "/api/memory/semantic/ingest", body)


def semantic_search(q, limit=5, doc_id=None):
    qs = f"?q={q}&limit={limit}"
    if doc_id:
        qs += f"&doc_id={doc_id}"
    return _req("GET", "/api/memory/semantic/search" + qs)


def semantic_docs():
    return _req("GET", "/api/memory/semantic/docs")
