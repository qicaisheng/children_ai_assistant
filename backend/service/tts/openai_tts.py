import time
import config
from utils import uuid_util
from openai import OpenAI
client = OpenAI()


def to_speech(text: str, voice_type: str = "alloy") -> str:
    output_audio_path = f"{config.audio_file_direction}/voice-{uuid_util.get_uuid4_no_hyphen()}.mp3"
    print(output_audio_path)

    tts_start_time = time.time()

    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_type,
        input=text
    )

    response.write_to_file(output_audio_path)

    tts_end_time = time.time()
    print(f"TTS time cost: {tts_end_time-tts_start_time}, tts_start_time={tts_start_time}, tts_end_time={tts_end_time}")

    print("TTS succeed, model: openai-tts-1")
    return output_audio_path
