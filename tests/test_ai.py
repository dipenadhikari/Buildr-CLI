from buildr_cli import ai


def test_configured_model_uses_documented_default(monkeypatch):
    monkeypatch.delenv("BUILDR_MODEL", raising=False)
    assert ai.configured_model() == "gpt-4.1-mini"


def test_has_api_key_is_false_when_empty(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "")
    assert ai.has_api_key() is False


def test_ask_openai_uses_responses_api(monkeypatch):
    calls = {}

    class FakeResponse:
        output_text = "Use a function and test it."

    class FakeResponses:
        def create(self, **kwargs):
            calls.update(kwargs)
            return FakeResponse()

    class FakeClient:
        responses = FakeResponses()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("openai.OpenAI", lambda api_key: FakeClient())

    result = ai.ask_openai("How should I structure this?", model="gpt-4.1-mini")

    assert result == "Use a function and test it."
    assert calls["model"] == "gpt-4.1-mini"
    assert calls["input"] == "How should I structure this?"
    assert "safe" in calls["instructions"]

