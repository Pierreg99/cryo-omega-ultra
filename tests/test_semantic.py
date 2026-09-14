from ultra import config, semantic


def test_ingest_and_search(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(config, "MEMORY_DIR", tmp_path / "memory")
    doc = semantic.ingest(
        "Frosthafen river ice. NEXCORP cryo logistics campus on the floodplain.\n\n"
        "Kira Valen investigates panel tableaus.",
        doc_id="frost-1",
        title="Frost notes",
    )
    assert doc["chunks"] >= 1
    assert doc["backend"] == "lexical"
    hits = semantic.search("NEXCORP cryo", limit=3)
    assert hits
    assert hits[0]["doc_id"] == "frost-1"
    assert semantic.delete_doc("frost-1") is True
