import importlib


def test_app_url_defaults_to_public_application(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")
    monkeypatch.delenv("APP_URL", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda: None)

    config = importlib.import_module("src.config")
    config = importlib.reload(config)

    assert config.APP_URL == "https://lappquiz.ict.unesp.br"


def test_app_url_uses_environment_override(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")
    monkeypatch.setenv("APP_URL", "https://quiz.example.com")

    config = importlib.import_module("src.config")
    config = importlib.reload(config)

    assert config.APP_URL == "https://quiz.example.com"
