import time
from app.core.story import Story
from app.service.asr.asr_service import recognize
from app.service.tts.tts_service import to_speech
import app.mqtt.publisher as mqtt_publisher
from app.service.conversation_service import stream_answer
import app.config as config
from app.core.role import Role, get_current_role
from app.core.conversation_message import save_message, Message, MessageType
from app.core.text_segmenter import segment_text
from app.core.intent_router import route, SemanticRouteResult
from app.core.user_intent import UserIntent
import app.service.rag.rag_story_wangwangdui as rag_story_wangwangdui
import app.core.story as core_story
from app.core.user import get_current_user

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
    _output_audio_url = []
    if semanticRouteResult.user_intent == UserIntent.RAG_QA_STORY:
        story = core_story.get_current_story()
        _output_text = rag_story_wangwangdui.answer(story=story, question=input_text)
        _url = await tts(text=_output_text, voice_type=role.voice_type)
        _output_audio_url.append(_url)
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=_url))
        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
    elif semanticRouteResult.user_intent == UserIntent.MAYBE_PLAY_STORY:
        _output_text = semanticRouteResult.arguments["output_text"]
        _url = await tts(text=_output_text, voice_type=role.voice_type)
        _output_audio_url.append(_url)
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=_url))
        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
    elif semanticRouteResult.user_intent == UserIntent.PLAY_STORY:
        story = semanticRouteResult.arguments["story"]
        assert isinstance(story, Story)
        core_story.set_current_story(story=story.name)
        if story.get_audio_urls():
            _order = 1
            _output_text = f"好的，现在播放{story.name}"
            _url = await tts(text=_output_text, voice_type=role.voice_type)
            mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=_order, url=_url))

            for _url in story.get_audio_urls():
                _order +=1
                _output_audio_url.append(_url)
                mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=_order, url=_url))
            mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=_order))
        else:
            _output_text = f"不好意思，很想给你播放{story.name}，但是暂时还没有找到这个音频内容。如果你想听的话，我可以给你讲讲大概的故事"
            _url = await tts(text=_output_text, voice_type=role.voice_type)
            _output_audio_url.append(_url)
            mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=_url))
    else:
        core_story.clear_current_story()
        stream_response = split_llm_response_and_tts(input_text=input_text, role=role)
        _order = 0
        _output_text = ""
        async for result in stream_response:
            print(result)
            _order = result["order"]
            _output_text += result["output_text"]
            _url = result["url"]
            _output_audio_url.append(_url)
            mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=_order, url=_url))

        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=_order))

    user = get_current_user()
    user_message = save_message(Message(user_id=user.id, role_code=role.code, message_type=MessageType.USER_MESSAGE, content=input_text, audio_id=[get_audio_file_name(audio_path)]))    
    assistant_mesage = save_message(Message(user_id=user.id, role_code=role.code, message_type=MessageType.ASSISTANT_MESSAGE, content=_output_text, audio_id=[get_audio_file_name(url) for url in _output_audio_url]))    
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
    output_audio_path = await to_speech(text, voice_type)
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