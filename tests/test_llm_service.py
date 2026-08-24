import importlib
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def llm_service(monkeypatch):
    monkeypatch.setenv("LITELLM_API_BASE_URL", "http://litellm-test:4000")
    monkeypatch.setenv("LITELLM_API_KEY", "test-litellm-key")
    monkeypatch.setenv("LITELLM_MODEL", "glm-4.7-flash:q4_K_M")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")
    monkeypatch.setenv("OPENROUTER_FALLBACK_MODEL", "nvidia/nemotron-3-nano-30b-a3b:nitro")
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


def test_evaluate_answer_uses_litellm(llm_service, monkeypatch):
    question = "Qual instrumento substituiu a broca manual?"
    correct_answer = "O motor odontológico"
    user_answer = "A turbina"
    mocked_primary = create_llm_mock("Resposta do professor")
    mocked_get_litellm = MagicMock(return_value=mocked_primary)
    mocked_get_fallback = MagicMock()
    monkeypatch.setattr(llm_service, "get_litellm_llm", mocked_get_litellm)
    monkeypatch.setattr(
        llm_service, "get_openrouter_fallback_llm", mocked_get_fallback
    )
    expected_prompt = llm_service.build_prompt(
        question, correct_answer, user_answer
    )

    result = llm_service.evaluate_answer(question, correct_answer, user_answer)

    mocked_get_litellm.assert_called_once_with()
    mocked_primary.invoke.assert_called_once_with(expected_prompt)
    mocked_get_fallback.assert_not_called()
    assert result == llm_service.clean_text_for_tts("Resposta do professor")


def test_evaluate_answer_uses_fallback_when_primary_fails(llm_service, monkeypatch):
    mocked_primary = MagicMock()
    mocked_primary.invoke.side_effect = RuntimeError("LiteLLM indisponível")
    mocked_fallback = create_llm_mock("Resposta do fallback")
    mocked_get_litellm = MagicMock(return_value=mocked_primary)
    mocked_get_fallback = MagicMock(return_value=mocked_fallback)
    monkeypatch.setattr(llm_service, "get_litellm_llm", mocked_get_litellm)
    monkeypatch.setattr(
        llm_service, "get_openrouter_fallback_llm", mocked_get_fallback
    )

    result = llm_service.evaluate_answer("Pergunta", "Correta", "Usuário")

    mocked_get_fallback.assert_called_once_with()
    mocked_fallback.invoke.assert_called_once()
    assert result == llm_service.clean_text_for_tts("Resposta do fallback")


def test_evaluate_answer_raises_on_both_failures(llm_service, monkeypatch):
    mocked_primary = MagicMock()
    mocked_primary.invoke.side_effect = RuntimeError("LiteLLM indisponível")
    mocked_fallback = MagicMock()
    mocked_fallback.invoke.side_effect = RuntimeError("OpenRouter indisponível")
    monkeypatch.setattr(
        llm_service,
        "get_litellm_llm",
        MagicMock(return_value=mocked_primary),
    )
    monkeypatch.setattr(
        llm_service,
        "get_openrouter_fallback_llm",
        MagicMock(return_value=mocked_fallback),
    )

    with pytest.raises(RuntimeError) as exc_info:
        llm_service.evaluate_answer("Pergunta", "Correta", "Usuário")

    message = str(exc_info.value)
    assert "ambos os provedores falharam" in message
    assert "LiteLLM indisponível" in message
    assert "OpenRouter indisponível" in message
