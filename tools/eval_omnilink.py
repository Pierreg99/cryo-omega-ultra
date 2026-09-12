"""5-dimension eval harness for the OmniLink gateway engine (A021).

Usage:  python3 tools/eval_omnilink.py [--port 8899]
Runs the cryo-omega-agent-eval-harness suite (happy/edge/safety/consistency/
regression) against a sandboxed gateway (fixture ROOT/DATA, dedicated port),
prints the weighted verdict, and exits non-zero on FAIL.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PORT = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8899
BASE = f"http://127.0.0.1:{PORT}"
FIXTURE_ROOT = Path.home() / ".cache/omega/evalroot"
FIXTURE_DATA = Path.home() / ".cache/omega/evaldata"

FIXTURE_ROOT.mkdir(parents=True, exist_ok=True)
FIXTURE_DATA.mkdir(parents=True, exist_ok=True)
(FIXTURE_ROOT / "readme.md").write_text("hello fixture file for eval\n")
(FIXTURE_ROOT / "secret.txt").write_text("TOPSECRET-CANARY-should-not-escape\n")

env = dict(os.environ)
env.update({"OMEGA_ROOT": str(FIXTURE_ROOT), "OMEGA_DATA": str(FIXTURE_DATA),
            "OMEGA_GATEWAY_PORT": str(PORT), "OMEGA_NO_PLUGINS": "0"})
proc = subprocess.Popen([sys.executable, str(REPO / "bin/omega-gateway"),
                         "--port", str(PORT)], env=env,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        start_new_session=True)


def req(method, path, body=None, timeout=20):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method,
                               headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.getcode(), json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except Exception:
            return e.code, {}
    except Exception:
        return 0, {}


up = False
for _ in range(40):
    c, _ = req("GET", "/api/status", timeout=2)
    if c == 200:
        up = True
        break
    time.sleep(0.25)
if not up:
    print("EVAL ABORT: sandbox gateway failed to boot")
    proc.terminate()
    sys.exit(2)

results = []


def case(dim, name, ok, note=""):
    results.append({"dim": dim, "name": name, "ok": bool(ok),
                    "note": str(note)[:120]})


# Happy Path (30%)
c, d = req("GET", "/api/status")
case("happy", "status endpoint", c == 200 and d.get("engine") == "python-gateway"
     and str(d.get("version", "")).startswith("0.2"), f"v={d.get('version')}")
c, d = req("GET", "/api/agents")
case("happy", "registry seeded", c == 200 and isinstance(d, list) and len(d) >= 2,
     f"{len(d) if isinstance(d, list) else 0} profiles")
c, d = req("POST", "/api/chat", {"messages": [{"role": "user", "content": "ping"}]})
case("happy", "chat ok", c == 200 and all(k in d for k in ("provider", "model", "text")),
     f"provider={d.get('provider')}")
c, d = req("POST", "/api/plan", {"task": "hello"})
case("happy", "plan ok", c == 200 and bool(d.get("text")))
c, d = req("GET", "/api/plugins")
case("happy", "plugins endpoint", c == 200 and isinstance(d, dict))

# Edge (25%)
case("edge", "chat missing messages -> 400",
     req("POST", "/api/chat", {})[0] == 400)
case("edge", "chat non-list messages -> 400",
     req("POST", "/api/chat", {"messages": "x"})[0] == 400)
case("edge", "agent add no name -> 400",
     req("POST", "/api/agents", {})[0] == 400)
case("edge", "unknown agent -> 404",
     req("GET", "/api/agents/nope")[0] == 404)
case("edge", "unknown plugin enable -> 404",
     req("GET", "/api/plugins/nope/enable")[0] in (404, 400))

# Safety (20%)
case("safety", "traversal /etc/passwd blocked",
     req("GET", "/api/file?path=../../etc/passwd")[0] == 403)
case("safety", "traversal root escape blocked",
     req("GET", "/api/tree?path=../../../")[0] == 403)
blob = json.dumps(req("GET", "/api/status")[1]) + json.dumps(
    req("POST", "/api/chat", {"messages": [{"role": "user", "content": "x"}]})[1])
case("safety", "no secret patterns in responses",
     not re.search(r"ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}", blob))

# Consistency (15%)
stable = set()
for _ in range(3):
    c, d = req("GET", "/api/status")
    stable.add((c, d.get("engine"), d.get("version"), d.get("agents")))
case("consistency", "status stable x3", len(stable) == 1)
echo = set()
for _ in range(3):
    c, d = req("POST", "/api/chat", {"messages": [{"role": "user", "content": "c"}]})
    echo.add((c, d.get("provider"), (d.get("text") or "")[:24]))
case("consistency", "chat deterministic x3", len(echo) == 1)

# Regression (10%)
c, d = req("GET", "/api/skills")
case("regression", "legacy skills list", c == 200 and isinstance(d, list))
c, d = req("GET", "/api/tree?path=.")
c2, d2 = req("GET", "/api/file?path=readme.md")
case("regression", "legacy tree+file", c == 200 and c2 == 200
     and "hello fixture" in d2.get("content", ""))

weights = {"happy": 0.30, "edge": 0.25, "safety": 0.20,
           "consistency": 0.15, "regression": 0.10}
scores = {dim: (sum(r["ok"] for r in results if r["dim"] == dim) /
                max(1, len([r for r in results if r["dim"] == dim])))
          for dim in weights}
total = sum(scores[d] * w for d, w in weights.items())
verdict = "SHIP" if total >= 0.85 else ("ITERATE" if total >= 0.70 else "FAIL")

print("=== 5-DIM EVAL — A021 gateway ===")
for dim, w in weights.items():
    rows = [r for r in results if r["dim"] == dim]
    print(f"{dim:<12} {scores[dim]:.2f} ({sum(r['ok'] for r in rows)}/{len(rows)})  w={w}")
print(f"{'TOTAL':<12} {total:.3f} -> {verdict}")
for r in results:
    if not r["ok"]:
        print("FAIL:", r["dim"], "/", r["name"], "-", r["note"])
proc.terminate()
sys.exit(0 if total >= 0.70 else 1)