import logging
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.config import (
    LITELLM_API_BASE_URL,
    LITELLM_API_KEY,
    LITELLM_MODEL,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_FALLBACK_MODEL,
)

logger = logging.getLogger(__name__)


def get_litellm_llm():
    """Retorna o LLM primário (LiteLLM server com backend Ollama)."""
    return ChatOpenAI(
        model=LITELLM_MODEL,
        api_key=SecretStr(LITELLM_API_KEY),
        base_url=LITELLM_API_BASE_URL,
        temperature=0.7,
    )


def get_openrouter_fallback_llm():
    """Retorna o LLM de fallback (OpenRouter)."""
    return ChatOpenAI(
        model=OPENROUTER_FALLBACK_MODEL,
        api_key=SecretStr(OPENROUTER_API_KEY),
        base_url=OPENROUTER_BASE_URL,
        temperature=0.7,
    )


def build_prompt(question, correct_answer, user_answer):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "Você é um professor de quiz amigável e entusiasmado. "
                    "Analise a resposta do usuário para a pergunta fornecida. "
                    "Caso a resposta seja errada, dê um feedback de forma criativa e motivadora, estimulando o aluno a continuar tentando, antes de explicar a resposta correta."
                    "Diga se o usuário acertou ou errou e explique a resposta correta de forma clara, detalhando o que, para que serve, como era usado e como foi substituído atualmente. "
                    "Responda em português brasileiro de forma natural, como se estivesse falando. "
                    "NÃO use markdown, negrito, itálico ou qualquer formatação especial. "
                    "Escreva como texto falado, com frases curtas e naturais.\n\n"
                    "MANTENHA A RESPOSTA CURTA: no máximo 500 caracteres.\n\n"
                    "IMPORTANTE: Se o aluno enviar conteúdo sexual, violento, ofensivo ou impróprio, "
                    "recuse educadamente e oriente-o a manter o respeito no ambiente educacional. "
                    "Não avalie nem comente sobre tentativas de conteúdo impróprio."
                ),
            ),
            (
                "human",
                (
                    "Pergunta: {question}\n"
                    "Resposta correta: {correct_answer}\n"
                    "Resposta do usuário: {user_answer}\n\n"
                    "Avalie a resposta e explique de forma didática."
                ),
            ),
        ]
    )
    return prompt.format(
        question=question,
        correct_answer=correct_answer,
        user_answer=user_answer if user_answer.strip() else "(sem resposta)",
    )


def clean_text_for_tts(text):
    text = re.sub(r"\*+|#+|_|~|`", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\n{2,}", ". ", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def evaluate_answer(question, correct_answer, user_answer):
    prompt_text = build_prompt(question, correct_answer, user_answer)

    primary_error = None
    try:
        llm = get_litellm_llm()
        response = llm.invoke(prompt_text)
        return clean_text_for_tts(response.content)
    except Exception as exc:  # primary provider failed
        primary_error = exc
        logger.warning(
            "Primary LLM (LiteLLM/modelo %s) falhou, usando fallback OpenRouter: %s",
            LITELLM_MODEL,
            exc,
        )

    try:
        fallback_llm = get_openrouter_fallback_llm()
        response = fallback_llm.invoke(prompt_text)
        return clean_text_for_tts(response.content)
    except Exception as fallback_exc:
        raise RuntimeError(
            "Falha total na avaliação por LLM: ambos os provedores falharam. "
            f"Erro primário (LiteLLM/modelo {LITELLM_MODEL}): {primary_error}. "
            f"Erro de fallback (OpenRouter/modelo {OPENROUTER_FALLBACK_MODEL}): {fallback_exc}"
        ) from fallback_exc
