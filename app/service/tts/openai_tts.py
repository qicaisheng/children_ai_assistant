import asyncio
import time
import app.config as config
from app.utils import uuid_util
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


async def ato_speech(text: str, voice_type: str = "alloy") -> str:
    output_audio_path = f"{config.audio_file_direction}/voice-{uuid_util.get_uuid4_no_hyphen()}.mp3"
    print(output_audio_path)
    file_to_save = open(output_audio_path, "wb")

    tts_start_time = time.time()

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice_type,
        input=text,
        response_format='mp3'
    ) as response:        
        for chunk in response.iter_bytes():
            file_to_save.write(chunk)

        file_to_save.close()

    tts_end_time = time.time()
    print(f"TTS time cost: {tts_end_time-tts_start_time}, tts_start_time={tts_start_time}, tts_end_time={tts_end_time}")

    print("TTS succeed, model: openai-tts-1")

    return output_audio_path


if __name__ == '__main__':
    to_speech("hello world, there are so many words, can you speak")
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(ato_speech("hello world, there are so many words, can you speak"))
