from ultra.llm import LLMResult, estimate_tokens


def test_estimate_tokens():
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("a" * 40) == 10
    assert estimate_tokens("") == 0


def test_llm_result_usage_fields():
    r = LLMResult("hi", prompt_tokens=2, completion_tokens=1)
    assert r.prompt_tokens == 2
    assert r.completion_tokens == 1
