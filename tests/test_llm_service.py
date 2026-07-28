import importlib
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def llm_service(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")
    return importlib.import_module("src.llm_service")


def create_llm_mock(response_content):
    llm_response = MagicMock()
    llm_response.content = response_content
    mocked_llm = MagicMock()
    mocked_llm.invoke.return_value = llm_response
    return mocked_llm


def test_build_prompt_contains_question_correct_answer_and_user_answer(llm_service):
    question = "Qual instrumento substituiu a broca manual?"
    correct_answer = "O motor odontológico"
    user_answer = "A turbina"

    prompt = llm_service.build_prompt(question, correct_answer, user_answer)

    assert question in prompt
    assert correct_answer in prompt
    assert user_answer in prompt


def test_build_prompt_marks_blank_user_answer_as_unanswered(llm_service):
    prompt = llm_service.build_prompt("Pergunta", "Resposta correta", "   ")

    assert "(sem resposta)" in prompt


def test_clean_text_for_tts_removes_markdown_and_normalizes_whitespace(
    llm_service,
):
    markdown_text = (
        "**Correto!** Veja [este link](https://example.com)\n\n"
        "## _Mais_   `detalhes` ~~agora~~"
    )

    cleaned_text = llm_service.clean_text_for_tts(markdown_text)

    assert cleaned_text == "Correto! Veja este link. Mais detalhes agora"


def test_evaluate_answer_invokes_mocked_llm_with_built_prompt(
    llm_service, monkeypatch
):
    question = "Qual instrumento substituiu a broca manual?"
    correct_answer = "O motor odontológico"
    user_answer = "A turbina"
    mocked_llm = create_llm_mock("Resposta do professor")
    mocked_get_llm = MagicMock(return_value=mocked_llm)
    monkeypatch.setattr(llm_service, "get_llm", mocked_get_llm)
    expected_prompt = llm_service.build_prompt(
        question, correct_answer, user_answer
    )

    llm_service.evaluate_answer(question, correct_answer, user_answer)

    mocked_get_llm.assert_called_once_with()
    mocked_llm.invoke.assert_called_once_with(expected_prompt)


def test_evaluate_answer_returns_cleaned_llm_response(
    llm_service, monkeypatch
):
    markdown_response = (
        "**Correto!**\n\nVeja   [a resposta](https://example.com)"
    )
    mocked_llm = create_llm_mock(markdown_response)
    monkeypatch.setattr(
        llm_service, "get_llm", MagicMock(return_value=mocked_llm)
    )

    result = llm_service.evaluate_answer("Pergunta", "Correta", "Usuário")

    assert result == llm_service.clean_text_for_tts(markdown_response)


def test_evaluate_answer_propagates_llm_exception(llm_service, monkeypatch):
    mocked_llm = MagicMock()
    mocked_llm.invoke.side_effect = RuntimeError("LLM indisponível")
    monkeypatch.setattr(
        llm_service, "get_llm", MagicMock(return_value=mocked_llm)
    )

    with pytest.raises(RuntimeError, match="LLM indisponível"):
        llm_service.evaluate_answer("Pergunta", "Correta", "Usuário")
