import asyncio
from service.streaming_asr_demo import recognize
from service.tts_websocket_demo import speak
import mqtt.publisher as mqtt_publisher
from service.conversation_service import no_stream_answer
import config
from core.role import get_current_role
from core.conversation_message import save_message, Message, MessageType

async def response_to_uploaded_audio(audio_path: str, recording_id: int):
    role = get_current_role()

    print(f"response_to_uploaded_audio: {audio_path}")
    input_text = await recognize(audio_path)

    if input_text == "":
        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=role.retry_voice))
        return

    print(f"ASR succeed, input_text: {input_text}")

    output_text = no_stream_answer(input_text, role.code)
    print(f"LLM succeed, output_text: {output_text}")

    output_audio_path = await speak(text=output_text, voice_type=role.voice_type)
    print(f"TTS succeed, output_audio_path: {output_audio_path}")

    mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
    mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=get_audio_url(output_audio_path)))

    user_message = save_message(Message(role_code=role.code, message_type=MessageType.USER_MESSAGE, content=input_text, audio_id=get_audio_file_name(audio_path)))    
    assistant_mesage = save_message(Message(role_code=role.code, message_type=MessageType.ASSISTANT_MESSAGE, content=output_text, audio_id=get_audio_file_name(output_audio_path)))    
    print(f"Save messages succeed, user_message: {user_message}, assistant_mesage: {assistant_mesage}")


def get_audio_url(path: str):
    file_name = get_audio_file_name(path)
    
    audio_url = config.audio_base_url + file_name
    
    return audio_url

def get_audio_file_name(path: str):
    file_name = path.split('/')[-1]
    return file_name


