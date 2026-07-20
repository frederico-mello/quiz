import os

from dotenv import load_dotenv

load_dotenv()

try:
    OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
except KeyError:
    raise ValueError(
        "OPENROUTER_API_KEY não configurada. "
        "Copie .env.example para .env e adicione sua chave."
    )

OPENROUTER_BASE_URL = os.environ.get(
    "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
)

LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek/deepseek-v4-flash")

MODERATION_ENABLED = os.environ.get("MODERATION_ENABLED", "true").lower() == "true"

APP_URL = os.environ.get("APP_URL", "http://localhost:8501")

# TTS settings
TTS_VOICE = os.environ.get("TTS_VOICE", "pt-BR-FranciscaNeural")
TEMP_AUDIO_DIR = os.environ.get("TEMP_AUDIO_DIR", "tmp/audio")
