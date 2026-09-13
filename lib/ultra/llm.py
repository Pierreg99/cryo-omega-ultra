"""CryoOmniRoute LLM layer — minimax-m3 default, failover chain, offline echo."""
import json
import urllib.error
import urllib.request

from . import config


class LLMResult:
    def __init__(self, text, provider="offline", model="echo", latency_ms=0):
        self.text = text
        self.provider = provider
        self.model = model
        self.latency_ms = latency_ms

    def __str__(self):
        return self.text


def _post(url, key, payload, model, provider):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    if provider == "anthropic":
        return "".join(c.get("text", "") for c in data.get("content", []))
    return data["choices"][0]["message"]["content"]


def chat(messages, provider=None, model=None, stream=False):
    """Send chat messages through the failover chain. Returns LLMResult."""
    cfg = config.load()
    wanted = provider or cfg.get("provider", "minimax")
    order = [wanted] + [p for p, _ in config.active_providers() if p != wanted]
    for name in order:
        spec = config.PROVIDERS[name]
        key = config.key_for(name)
        if not key:
            continue
        url = spec["base"].rstrip("/") + "/chat/completions"
        use_model = model or cfg.get("model") or spec["model"]
        payload = {"model": use_model, "messages": messages, "stream": False}
        try:
            text = _post(url, key, payload, use_model, name)
            return LLMResult(text, name, use_model)
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, OSError):
            continue
    last = messages[-1]["content"] if messages else ""
    if cfg.get("offline_echo", True):
        echo = (
            "⟦CRYOMEGA ULTRA·OFFLINE⟧ No provider key detected "
            "(set CRYOMEGA_MINIMAX_KEY etc.). Echo mode.\n"
            f"‣ you: {last}\n"
            "‣ run `omega doctor` to wire minimax-m3."
        )
        return LLMResult(echo)
    raise RuntimeError("no provider available and offline echo disabled")


def complete(prompt, **kw):
    return chat([{"role": "user", "content": prompt}], **kw)
