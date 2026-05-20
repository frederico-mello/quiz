import asyncio
import os
import tempfile
import edge_tts
from mutagen.mp3 import MP3
from src.config import TTS_VOICE, TEMP_AUDIO_DIR


async def generate_speech_async(text, output_path, voice=TTS_VOICE):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_speech(text):
    os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(suffix=".mp3", dir=TEMP_AUDIO_DIR)
    os.close(fd)

    try:
        asyncio.run(generate_speech_async(text, tmp_path))
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise RuntimeError(f"Falha ao gerar áudio TTS: {e}")

    return tmp_path


def get_audio_duration(filepath):
    audio = MP3(filepath)
    return audio.info.length
