import time
from core.story import Story
from service.asr.streaming_asr_demo import recognize
from service.tts.tts_websocket_demo import speak
import mqtt.publisher as mqtt_publisher
from service.conversation_service import stream_answer
import config
from core.role import Role, get_current_role
from core.conversation_message import save_message, Message, MessageType
from core.text_segmenter import segment_text
from core.intent_router import route, SemanticRouteResult
from core.user_intent import UserIntent


async def split_response_to_uploaded_audio(audio_path: str, recording_id: int):
    role = get_current_role()

    print(f"split_response_to_uploaded_audio: {audio_path}")
    asr_start_time = time.time()
    input_text = await recognize(audio_path)
    asr_end_time = time.time()
    print(f"ASR time cost: {asr_end_time-asr_start_time}, asr_start_time={asr_start_time}, asr_end_time={asr_end_time}")

    if input_text == "":
        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=role.retry_voice))
        return

    print(f"ASR succeed, input_text: {input_text}")

    await process_user_input_text(audio_path, recording_id, role, input_text)

async def process_user_input_text(audio_path, recording_id, role, input_text):
    semanticRouteResult = route(input_text)
    if semanticRouteResult.user_intent == UserIntent.MAYBE_PLAY_STORY:
        _output_text = semanticRouteResult.arguments["output_text"]
        _url = await tts(text=_output_text, voice_type=role.voice_type)
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=_url))
        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
    elif semanticRouteResult.user_intent == UserIntent.PLAY_STORY:
        story = semanticRouteResult.arguments["story"]
        assert isinstance(story, Story)

        if story.get_audio_urls():
            _order = 1
            _output_text = f"好的，现在播放{story.name}"
            _url = await tts(text=_output_text, voice_type=role.voice_type)
            mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=_order, url=_url))

            for _url in story.get_audio_urls():
                _order +=1
                mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=_order, url=_url))
            mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=_order))
        else:
            _output_text = f"不好意思，很想给你播放{story.name}，但是暂时还没有找到这个音频内容。如果你想听的话，我可以给你讲讲大概的故事"
            _url = await tts(text=_output_text, voice_type=role.voice_type)
            mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=_url))
    else:
        stream_response = split_llm_response_and_tts(input_text=input_text, role=role)
        _order = 0
        _output_text = ""
        async for result in stream_response:
            print(result)
            _order = result["order"]
            _output_text = result["output_text"]
            _url = result["url"]

            mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=_order, url=_url))

        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=_order))

    user_message = save_message(Message(role_code=role.code, message_type=MessageType.USER_MESSAGE, content=input_text, audio_id=get_audio_file_name(audio_path)))    
    assistant_mesage = save_message(Message(role_code=role.code, message_type=MessageType.ASSISTANT_MESSAGE, content=_output_text, audio_id=None))    
    print(f"Save messages succeed, user_message: {user_message}, assistant_mesage: {assistant_mesage}")


async def split_llm_response_and_tts(input_text: str, role: Role):
    stream_response = stream_answer(input_text, role_code=role.code)

    segments = segment_text(stream_response, segment_size=2)
    
    output_texts = ""
    _order = 0

    for segment in segments:
        output_texts += segment
        print(f"output_texts: {output_texts}")
        print(f"order: {_order}, tts_text: {segment}")

        url = await tts(text=segment, voice_type=role.voice_type)
        _order += 1
        result = {"url": url, "order": _order, "output_text": segment}
        yield result

async def tts(text, voice_type) -> str:
    tts_start_time = time.time()
    output_audio_path = await speak(text, voice_type)
    tts_end_time = time.time()
    print(f"TTS succeed, output_audio_path: {output_audio_path}")
    print(f"TTS time cost: {tts_end_time-tts_start_time}, tts_start_time={tts_start_time}, tts_end_time={tts_end_time}")

    return get_audio_url(output_audio_path)


def get_audio_url(path: str):
    file_name = get_audio_file_name(path)
    
    audio_url = config.audio_base_url + file_name
    
    return audio_url

def get_audio_file_name(path: str):
    file_name = path.split('/')[-1]
    return file_name

def get_audio_url_from_id(id: str):
    return config.audio_base_url + id
