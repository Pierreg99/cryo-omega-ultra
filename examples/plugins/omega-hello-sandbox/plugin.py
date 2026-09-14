"""Sandbox plugin — no in-process register(); only handle(event)."""


def handle(event: dict) -> dict:
    return {
        "plugin": "omega-hello-sandbox",
        "message": "hello from subprocess sandbox",
        "method": event.get("method"),
        "path": event.get("path"),
        "status": 200,
    }
