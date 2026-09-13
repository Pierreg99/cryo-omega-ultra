from ultra import observability


def test_request_id_stable_incoming():
    assert observability.new_request_id("abc123") == "abc123"
    assert len(observability.new_request_id(None)) == 16


def test_redact_secrets():
    s = observability.redact("Authorization: Bearer sk-secret Authorization=Bearer x")
    assert "sk-secret" not in s
    assert "REDACTED" in s


def test_metrics_record():
    before = observability.snapshot()["requests"]
    observability.record_request(ok=True, latency_ms=12, kind="chat", request_id="r1")
    snap = observability.snapshot()
    assert snap["requests"] == before + 1
    assert snap["chat_calls"] >= 1
    assert snap["last_latency_ms"] == 12
