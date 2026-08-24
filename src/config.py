import os

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Variáveis obrigatórias (LiteLLM primário + OpenRouter fallback)
# ---------------------------------------------------------------------------
REQUIRED_ENV_VARS = {
    "LITELLM_API_BASE_URL": "URL do LiteLLM server (ex.: http://localhost:4000)",
    "LITELLM_API_KEY": "Chave virtual de autenticação no LiteLLM server",
    "LITELLM_MODEL": "Modelo primário (ex.: glm-4.7-flash:q4_K_M)",
    "OPENROUTER_API_KEY": "Chave de API do OpenRouter (fallback)",
    "OPENROUTER_FALLBACK_MODEL": "Modelo de fallback (ex.: nvidia/nemotron-3-nano-30b-a3b:nitro)",
}


def validate_config():
    """Valida que todas as variáveis de ambiente obrigatórias estão definidas.

    Chamada no startup da aplicação; não é executada em import-time para
    permitir que ferramentas e scripts auxiliares importem ``src.*`` sem um
    ``.env`` completo. Defina ``SKIP_CONFIG_VALIDATION=1`` para pular.
    """
    if os.environ.get("SKIP_CONFIG_VALIDATION") == "1":
        return
    missing = [
        f"{name} ({description})"
        for name, description in REQUIRED_ENV_VARS.items()
        if not os.environ.get(name)
    ]
    if missing:
        raise ValueError(
            "Variáveis de ambiente obrigatórias ausentes: "
            + ", ".join(missing)
            + ". Copie .env.example para .env e preencha os valores."
        )


# Define as constantes (podem ser vazias se SKIP_CONFIG_VALIDATION=1).
LITELLM_API_BASE_URL = os.environ.get("LITELLM_API_BASE_URL", "")
LITELLM_API_KEY = os.environ.get("LITELLM_API_KEY", "")
LITELLM_MODEL = os.environ.get("LITELLM_MODEL", "")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_FALLBACK_MODEL = os.environ.get("OPENROUTER_FALLBACK_MODEL", "")
OPENROUTER_BASE_URL = os.environ.get(
    "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
)

MODERATION_ENABLED = os.environ.get("MODERATION_ENABLED", "true").lower() == "true"

APP_URL = os.environ.get("APP_URL", "https://lappquiz.ict.unesp.br")

# TTS settings
TTS_VOICE = os.environ.get("TTS_VOICE", "pt-BR-FranciscaNeural")
TEMP_AUDIO_DIR = os.environ.get("TEMP_AUDIO_DIR", "tmp/audio")
