import pytest
from ultra import config, memory


@pytest.fixture(autouse=True)
def _mem_tmp(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(config, "MEMORY_DIR", tmp_path / "memory")
    monkeypatch.setattr(config, "MEMORY_WORKING_DIR", tmp_path / "memory" / "working")


def test_append_load_forget():
    memory.append_turn("s1", role="user", content="hi", source="test")
    memory.append_turn("s1", role="assistant", content="hello", source="test")
    turns = memory.load_turns("s1")
    assert len(turns) == 2
    assert turns[0]["provenance"]["source"] == "test"
    assert memory.list_sessions() == ["s1"]
    assert memory.forget("s1") is True
    assert memory.load_turns("s1") == []


def test_bad_session_id():
    with pytest.raises(ValueError):
        memory.append_turn("../x", role="user", content="no")


def test_messages_for_chat():
    memory.append_turn("a", role="user", content="u1")
    memory.append_turn("a", role="assistant", content="a1")
    msgs = memory.messages_for_chat("a")
    assert msgs == [
        {"role": "user", "content": "u1"},
        {"role": "assistant", "content": "a1"},
    ]
