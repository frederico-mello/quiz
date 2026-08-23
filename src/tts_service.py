import asyncio
import os
import tempfile
import time
import edge_tts
from src.config import TTS_VOICE, TEMP_AUDIO_DIR

STALE_AUDIO_SECONDS = 24 * 60 * 60


def _cleanup_stale_audio():
    try:
        if not os.path.isdir(TEMP_AUDIO_DIR):
            return
        cutoff = time.time() - STALE_AUDIO_SECONDS
        for name in os.listdir(TEMP_AUDIO_DIR):
            path = os.path.join(TEMP_AUDIO_DIR, name)
            try:
                if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
                    os.remove(path)
            except OSError:
                pass
    except OSError:
        pass


async def generate_speech_async(text, output_path, voice=TTS_VOICE):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_speech(text):
    os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
    _cleanup_stale_audio()
    fd, tmp_path = tempfile.mkstemp(suffix=".mp3", dir=TEMP_AUDIO_DIR)
    os.close(fd)

    try:
        asyncio.run(generate_speech_async(text, tmp_path))
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise RuntimeError(f"Falha ao gerar áudio TTS: {e}")

    return tmp_path

