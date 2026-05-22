import re
from typing import Optional, Tuple

BLOCKED_KEYWORDS = {
    # Portuguese sexual
    "buceta",
    "piroca",
    "caralho",
    "cu",
    "cuzão",
    "foda",
    "foder",
    "pinto",
    "xota",
    "bunda",
    "bunda mole",
    "merda",
    "puta",
    "vadia",
    "zorra",
    "rola",
    "fresco",
    "viado",
    "bicha",
    "sodomia",
    "orgia",
    "pornô",
    "pornografia",
    "sexo",
    "sexual",
    "vagina",
    "pênis",
    "penis",
    "buro",
    "baba",
    "lança",
    "rola",
    "piroca",
    "bicha",
    # Portuguese violent
    "matar",
    "morte",
    "morrer",
    "estuprar",
    "estupro",
    "violar",
    "violência",
    "agredir",
    "agressão",
    "tortura",
    "torturar",
    "mutilar",
    "decapitar",
    "decapitação",
    "massacre",
    "assassinar",
    "assassino",
    "genocídio",
    "genocidio",
    "suicídio",
    "suicidio",
    "enforcar",
    "enforcamento",
    "arma",
    "armar",
    "bomba",
    "explosivo",
    "atirar",
    "atropelar",
    "apunhalar",
    "estrangular",
    "envenenar",
    "veneno",
    "maldição",
    "maldicao",
    # English sexual
    "fuck",
    "shit",
    "ass",
    "bitch",
    "bastard",
    "dick",
    "pussy",
    "cock",
    "cunt",
    "penis",
    "vagina",
    "nipple",
    "naked",
    "nude",
    "porn",
    "xxx",
    "erotic",
    "fetish",
    "slut",
    "whore",
    "hooker",
    "prostitute",
    "stripper",
    # English violent
    "kill",
    "death",
    "die",
    "murder",
    "rape",
    "rapist",
    "stab",
    "gun",
    "shoot",
    "bomb",
    "explode",
    "explosion",
    "terrorist",
    "terrorism",
    "massacre",
    "slit",
    "throat",
    "strangle",
    "torture",
    "torturing",
    "behead",
    "decapitate",
}

BLOCKED_PATTERNS = [
    r"(?i)\b(n|i|v|o)\s*({v1})\s*({v2})\s*({v3})\b",
    r"(?i)\bporra\b",
    r"(?i)\bdemerol\b",
    r"(?i)\b毙\b",
]

LEET_SPEAK_MAP = str.maketrans("aeiou43", "aeiou38")


def normalize_leet(text: str) -> str:
    return text.translate(LEET_SPEAK_MAP).lower()


def check_patterns(text: str) -> Optional[str]:
    normalized = normalize_leet(text)
    for pattern in BLOCKED_PATTERNS:
        try:
            if re.search(pattern, normalized, re.IGNORECASE):
                return "Conteúdo contém padrão bloqueado."
        except re.error:
            pass
    return None


def check_keywords(text: str) -> Tuple[bool, Optional[str]]:
    normalized = normalize_leet(text)
    for keyword in BLOCKED_KEYWORDS:
        if keyword in normalized:
            return True, f"Termo impróprio detectado: '{keyword}'"
    return False, None


def check_text_local(text: str) -> Tuple[bool, Optional[str]]:
    blocked, msg = check_keywords(text)
    if blocked:
        return True, msg
    pattern_msg = check_patterns(text)
    if pattern_msg:
        return True, pattern_msg
    return False, None


def check_text_llm(text: str, llm) -> Tuple[bool, Optional[str]]:
    from src.config import LLM_MODEL, OPENROUTER_API_KEY, OPENROUTER_BASE_URL

    if not OPENROUTER_API_KEY:
        return False, None

    from langchain_openai import ChatOpenAI
    from pydantic import SecretStr

    llm_client = ChatOpenAI(
        model=LLM_MODEL,
        api_key=SecretStr(OPENROUTER_API_KEY),
        base_url=OPENROUTER_BASE_URL,
        temperature=0.1,
        extra_body={
            "provider": {
                "order": ["DeepInfra", "Together"],
                "allow_fallbacks": True,
            }
        },
    )

    moderation_prompt = (
        "Você é um moderador de conteúdo. Analise o texto abaixo e determine "
        "se ele contém conteúdo SEXUAL ou OFENSIVO direcionado a terceiros."
        "Exceção: o quiz trata de instrumentos da área da saúde. Portanto, as respostas podem "
        "conter palavras ou expressões relacionadas a procedimentos médicos e odontológicos, "
        "como perfuração de crânio, cirurgia, sangue. \n\n"
        f"Texto: {text}\n\n"
        "Responda apenas com uma das seguintes opções (sem explicação):\n"
        "- SEGURO: o texto é apropiado para um ambiente educacional\n"
        "- BLOQUEAR: o texto contém conteúdo sexual, violento ou ofensivo\n\n"
        "Resposta:"
    )

    response = llm_client.invoke(moderation_prompt)
    raw = response.content
    if isinstance(raw, list):
        content = "".join(
            block if isinstance(block, str) else block.get("text", "") for block in raw
        )
    else:
        content = raw
    content = content.strip().lower()

    if content.startswith("bloquear"):
        return True, "Conteúdo impróprio identificado pela moderação semântica."
    return False, None


def check_text(text: str, use_llm: bool = True) -> Tuple[bool, Optional[str]]:
    blocked, msg = check_text_local(text)
    if blocked:
        return True, msg

    if use_llm:
        try:
            from src.llm_service import get_llm

            llm = get_llm()
            blocked_llm, msg_llm = check_text_llm(text, llm)
            return blocked_llm, msg_llm
        except Exception:
            pass

    return False, None


def get_warning_level(warnings: int) -> str:
    if warnings == 0:
        return "none"
    elif warnings == 1:
        return "first"
    elif warnings == 2:
        return "second"
    else:
        return "blocked"
