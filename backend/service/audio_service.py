from service.streaming_asr_demo import recognize
from service.tts_websocket_demo import speak
import mqtt.publisher as mqtt_publisher

async def response_to_uploaded_audio(audio_path: str):
    print(f"response_to_uploaded_audio: {audio_path}")
    input_text = recognize(audio_path)
    print(f"ASR succeed, input_text: {input_text}")
    output_audio_path = await speak(text=input_text)
    print(f"TTS succeed, output_audio_path: {output_audio_path}")

    recordingId = 1
    mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recordingId, order=1, url=get_audio_url(output_audio_path)))

def get_audio_url(path: str): 
    return ""


