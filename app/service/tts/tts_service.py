import asyncio
import time
import app.config as config
from app.service.tts.tts import TTS
import app.service.tts.volcengine_websocket_tts as volcengine_tts
import app.service.tts.openai_tts as openai_tts


async def to_speech(text: str, voice_type: str = None) -> str:
    tts_start_time = time.time()

    if config.tts == TTS.VOLCENGINE:
        if voice_type is None:
            voice_type = "BV001_streaming"
        output_audio_path = await volcengine_tts.speak(text=text, voice_type=voice_type)
    
    elif config.tts == TTS.OPENAI:
        # if voice_type is None:
        voice_type = "alloy"
        output_audio_path = openai_tts.to_speech(text=text, voice_type=voice_type)    
    else:
        raise ValueError("Unsupported TTS engine specified in config.")

    tts_end_time = time.time()
    print(f"TTS time cost: {tts_end_time-tts_start_time}, tts_start_time={tts_start_time}, tts_end_time={tts_end_time}")

    print(f"TTS succeed, model: {config.tts.value}, output_audio_path: {output_audio_path}")

    return output_audio_path


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(to_speech("你好，今天星期几"))
#     # loop.run_until_complete(to_speech("你好，今天星期几", voice_type="BV061_streaming"))
