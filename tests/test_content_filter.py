from unittest.mock import MagicMock

import pytest

import src.content_filter as content_filter
from src.content_filter import (
    check_keywords,
    check_patterns,
    check_text_local,
    check_text_llm,
    get_warning_level,
    normalize_leet,
)


def test_check_keywords_pt_sexual_term_is_blocked():
    blocked, msg = check_keywords("buceta")

    assert blocked is True
    assert msg is not None
    assert "buceta" in msg


def test_check_keywords_clean_text_returns_false():
    blocked, msg = check_keywords("olá mundo, tudo bem?")

    assert blocked is False
    assert msg is None


def test_check_keywords_leet_normalization_detects_blocked_word():
    blocked, msg = check_keywords("FODA")

    assert blocked is True
    assert msg is not None
    assert "foda" in msg


def test_check_patterns_blocks_matching_pattern():
    result = check_patterns("porra")

    assert result == "Conteúdo contém padrão bloqueado."


@pytest.mark.parametrize("count, level", [
    (0, "none"),
    (1, "first"),
    (2, "second"),
    (3, "blocked"),
])
def test_get_warning_level_escalates_per_count(count, level):
    assert get_warning_level(count) == level


@pytest.mark.parametrize("text, category", [
    ("foda", "pt-sexual"),
    ("matar", "pt-violent"),
    ("fuck", "en-sexual"),
    ("kill", "en-violent"),
])
def test_check_keywords_blocks_term_in_each_category(text, category):
    blocked, msg = check_keywords(text)

    assert blocked is True, f"expected block for {category} term {text!r}"
    assert msg is not None
    assert text in msg


def test_normalize_leet_lowercases_input():
    assert normalize_leet("FODA") == "foda"


def test_normalize_leet_applies_digit_translation_table():
    assert normalize_leet("4") == "3"
    assert normalize_leet("3") == "8"


def test_check_patterns_clean_text_returns_none():
    assert check_patterns("olá mundo") is None


def test_check_text_local_returns_keyword_block_for_blocked_term():
    blocked, msg = check_text_local("buceta")

    assert blocked is True
    assert msg is not None
    assert "buceta" in msg


def test_check_text_local_returns_pattern_block_when_keywords_clean():
    blocked, msg = check_text_local("porra")

    assert blocked is True
    assert msg == "Conteúdo contém padrão bloqueado."


def test_check_text_local_returns_clean_tuple_for_clean_text():
    blocked, msg = check_text_local("olá mundo, tudo bem?")

    assert blocked is False
    assert msg is None


def test_check_text_llm_blocks_mocked_llm_classification():
    llm_response = MagicMock()
    llm_response.content = "BLOQUEAR"
    mocked_llm = MagicMock()
    mocked_llm.invoke.return_value = llm_response

    blocked, msg = check_text_llm("texto ambíguo", mocked_llm)

    assert blocked is True
    assert msg == "Conteúdo impróprio identificado pela moderação semântica."


def test_check_text_skips_llm_when_text_is_blocked_locally(monkeypatch):
    mocked_check_text_llm = MagicMock()
    monkeypatch.setattr(content_filter, "check_text_llm", mocked_check_text_llm)

    blocked, msg = content_filter.check_text("buceta")

    assert blocked is True
    assert msg is not None
    mocked_check_text_llm.assert_not_called()


def test_check_text_invokes_llm_once_for_clean_text(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-api-key")
    from src import llm_service

    mocked_llm = MagicMock()
    monkeypatch.setattr(llm_service, "get_llm", MagicMock(return_value=mocked_llm))
    mocked_check_text_llm = MagicMock(return_value=(False, None))
    monkeypatch.setattr(content_filter, "check_text_llm", mocked_check_text_llm)

    result = content_filter.check_text("olá mundo", use_llm=True)

    assert result == (False, None)
    mocked_check_text_llm.assert_called_once_with("olá mundo", mocked_llm)


def test_check_text_skips_llm_when_disabled(monkeypatch):
    mocked_check_text_llm = MagicMock()
    monkeypatch.setattr(content_filter, "check_text_llm", mocked_check_text_llm)

    result = content_filter.check_text("olá mundo", use_llm=False)

    assert result == (False, None)
    mocked_check_text_llm.assert_not_called()
