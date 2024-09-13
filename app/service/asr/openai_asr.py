import time
from openai import OpenAI



def recognize(audio_path: str) -> str:
    asr_start_time = time.time()

    audio_file= open(audio_path, "rb")
    client = OpenAI()
    
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    asr_end_time = time.time()
    print(f"ASR time cost: {asr_end_time-asr_start_time}, asr_start_time={asr_start_time}, asr_end_time={asr_end_time}")
   
    output_text = transcription.text
    print(f"ASR succeed, model: openai-whisper-1, text: {output_text}")
    return output_text

# recognize("../audio/recording-2ddcd8b7238340c18a0c708082481c89.wav")
