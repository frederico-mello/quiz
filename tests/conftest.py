import json
import os

import pytest


@pytest.fixture(autouse=True)
def _required_llm_env(monkeypatch):
    """Garante que as variáveis de ambiente obrigatórias do src.config estejam definidas."""
    monkeypatch.setenv("SKIP_CONFIG_VALIDATION", "1")
    defaults = {
        "LITELLM_API_BASE_URL": "http://litellm-test:4000",
        "LITELLM_API_KEY": "test-litellm-key",
        "LITELLM_MODEL": "glm-4.7-flash:q4_K_M",
        "OPENROUTER_API_KEY": "test-api-key",
        "OPENROUTER_FALLBACK_MODEL": "nvidia/nemotron-3-nano-30b-a3b:nitro",
    }
    for key, value in defaults.items():
        if os.environ.get(key) is None:
            monkeypatch.setenv(key, value)


@pytest.fixture
def sample_questions():
    return [
        {"id": 1, "question": "Pergunta 1", "correct_answer": "Resposta 1"},
        {"id": 2, "question": "Pergunta 2", "correct_answer": "Resposta 2"},
        {"id": 3, "question": "Pergunta 3", "correct_answer": "Resposta 3"},
    ]


@pytest.fixture
def tmp_json_file(tmp_path):
    def factory(data, name="data.json"):
        path = tmp_path / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    return factory