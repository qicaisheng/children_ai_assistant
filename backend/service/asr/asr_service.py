import asyncio
import time
import config
from service.asr.asr import ASR
import service.asr.openai_asr as openai_asr
import service.asr.volcengine_streaming_asr as volcengine_asr

async def recognize(audio_path: str) -> str:
    output_text: str
    asr_start_time = time.time()
    if config.asr == ASR.VOLCENGINE:
        output_text = await volcengine_asr.recognize(audio_path=audio_path)
    elif config.asr == ASR.OPENAI:
        output_text = openai_asr.recognize(audio_path=audio_path)
    else:
        raise ValueError("Unsupported ASR engine specified in config.")

    asr_end_time = time.time()
    print(f"ASR time cost: {asr_end_time-asr_start_time}, asr_start_time={asr_start_time}, asr_end_time={asr_end_time}")
    print(f"ASR succeed, model: {config.asr.value}, text: {output_text}")

    return output_text

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(recognize("../audio/recording-2ddcd8b7238340c18a0c708082481c89.wav"))