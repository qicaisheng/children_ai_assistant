import asyncio
from service.streaming_asr_demo import recognize
from service.tts_websocket_demo import speak
import mqtt.publisher as mqtt_publisher
from conversation import no_stream_answer
import config
from core.role import get_current_role

async def response_to_uploaded_audio(audio_path: str, recording_id: int):
    print(f"response_to_uploaded_audio: {audio_path}")
    input_text = await recognize(audio_path)

    if input_text == "":
        role = get_current_role()
        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=role.retry_voice))
        return

    print(f"ASR succeed, input_text: {input_text}")

    output_text = no_stream_answer(input_text)
    print(f"LLM succeed, output_text: {output_text}")

    output_audio_path = await speak(text=output_text)
    print(f"TTS succeed, output_audio_path: {output_audio_path}")

    mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
    mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=get_audio_url(output_audio_path)))


def get_audio_url(path: str):
    file_name = path.split('/')[-1]
    
    audio_url = config.audio_base_url + file_name
    
    return audio_url


