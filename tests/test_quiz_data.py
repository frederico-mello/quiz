import json

import pytest

from src.quiz_data import get_question, get_question_by_id, load_questions


def test_load_questions_returns_list_from_valid_json(tmp_json_file):
    path = tmp_json_file([{"id": 1, "question": "Q", "correct_answer": "A"}])

    result = load_questions(str(path))

    assert result == [{"id": 1, "question": "Q", "correct_answer": "A"}]


def test_load_questions_raises_on_invalid_json(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_questions(str(path))


@pytest.mark.parametrize("index", [0, 1, 2])
def test_get_question_valid_index_returns_question(sample_questions, index):
    result = get_question(sample_questions, index)

    assert result == sample_questions[index]


@pytest.mark.parametrize("index", [-1, -100])
def test_get_question_negative_index_returns_none(sample_questions, index):
    assert get_question(sample_questions, index) is None


@pytest.mark.parametrize("index", [3, 4, 999])
def test_get_question_out_of_bounds_returns_none(sample_questions, index):
    assert get_question(sample_questions, index) is None


@pytest.mark.parametrize("question_id", [1, 2, 3])
def test_get_question_by_id_existing_returns_question(sample_questions, question_id):
    result = get_question_by_id(sample_questions, question_id)

    assert result == {"id": question_id, "question": f"Pergunta {question_id}", "correct_answer": f"Resposta {question_id}"}


@pytest.mark.parametrize("question_id", [0, 4, 999])
def test_get_question_by_id_missing_returns_none(sample_questions, question_id):
    assert get_question_by_id(sample_questions, question_id) is None