import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
LLM_MODEL = "deepseek/deepseek-v4-flash"
TTS_VOICE = "pt-BR-FranciscaNeural"
TEMP_AUDIO_DIR = "tmp"
MODERATION_ENABLED = True

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY não configurada. "
        "Copie .env.example para .env e adicione sua chave."
    )
