import json

import pytest


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