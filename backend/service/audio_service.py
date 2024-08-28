import asyncio
import aiohttp
import os
import time
from service.streaming_asr_demo import recognize
from service.tts_websocket_demo import speak
import mqtt.publisher as mqtt_publisher
from service.conversation_service import no_stream_answer, stream_answer
import config
from core.role import Role, get_current_role
from core.conversation_message import save_message, Message, MessageType
from core.text_segmenter import split_text, segment_text

async def response_to_uploaded_audio(audio_path: str, recording_id: int):
    role = get_current_role()

    print(f"response_to_uploaded_audio: {audio_path}")
    asr_start_time = time.time()
    input_text = await recognize(audio_path)
    asr_end_time = time.time()
    print(f"ASR time cost: {asr_end_time-asr_start_time}, asr_start_time={asr_start_time}, asr_end_time={asr_end_time}")

    if input_text == "":
        mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=1))
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=1, url=role.retry_voice))
        return

    print(f"ASR succeed, input_text: {input_text}")

    llm_start_time = time.time()
    output_texts = no_stream_answer(input_text, role.code)
    llm_end_time = time.time()
    print(f"LLM succeed, output_text: {output_texts}")
    print(f"LLM time cost: {llm_end_time-llm_start_time}, llm_start_time={llm_start_time}, llm_end_time={llm_end_time}")

    mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=len(output_texts)))
    _order = 0
    for output_text in output_texts:
        tts_start_time = time.time()
        output_audio_path = await speak(text=output_text, voice_type=role.voice_type)
        tts_end_time = time.time()
        print(f"TTS succeed, output_audio_path: {output_audio_path}")
        print(f"TTS time cost: {tts_end_time-tts_start_time}, tts_start_time={tts_start_time}, tts_end_time={tts_end_time}")

        _order += 1
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=_order, url=get_audio_url(output_audio_path)))

    user_message = save_message(Message(role_code=role.code, message_type=MessageType.USER_MESSAGE, content=input_text, audio_id=get_audio_file_name(audio_path)))    
    assistant_mesage = save_message(Message(role_code=role.code, message_type=MessageType.ASSISTANT_MESSAGE, content="".join(output_texts), audio_id=get_audio_file_name(output_audio_path)))    
    print(f"Save messages succeed, user_message: {user_message}, assistant_mesage: {assistant_mesage}")

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

    stream_response = split_llm_response_and_tts(input_text=input_text, role=role)
    _order = 0
    _output_text = ""
    async for result in stream_response:
        print(result)
        _order = result["order"]
        _output_text = result["output_text"]
        _url = result["url"]
        _path = result["path"]
        # await asyncio.sleep(2)

        if os.path.exists(_path) and os.path.getsize(_path) > 0:
            print("------------Audio file generate succeed---------------------------")
            print(f"File path: {_path}, Size: {os.path.getsize(_path)}")
            print(f"File URL: {_url}")
        else:
            print("------------Audio file generate failed---------------------------")
            print(f"File path: {_path}, Size: {os.path.getsize(_path)}")
            print(f"File URL: {_url}")
        # await check_file_url(_url)
        mqtt_publisher.audio_play(mqtt_publisher.AudioPlay(recordingId=recording_id, order=_order, url=_url))

    mqtt_publisher.audio_play_cmd(mqtt_publisher.AudioPlayCMD(recordingId=recording_id, total=_order))

    user_message = save_message(Message(role_code=role.code, message_type=MessageType.USER_MESSAGE, content=input_text, audio_id=get_audio_file_name(audio_path)))    
    assistant_mesage = save_message(Message(role_code=role.code, message_type=MessageType.ASSISTANT_MESSAGE, content=_output_text, audio_id=None))    
    print(f"Save messages succeed, user_message: {user_message}, assistant_mesage: {assistant_mesage}")

async def check_file_url(url: str):
    # await asyncio.sleep(5) 
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content_length = response.headers.get('Content-Length')
                    if content_length:
                        content_length = int(content_length)
                    else:
                        content_length = 0

                    if content_length > 0:
                        print(f"File at {url} is available and has size {content_length} bytes.")
                    else:
                        print(f"File at {url} is available but size is 0 bytes.")
                else:
                    print(f"Failed to download file from {url}. Status code: {response.status}")
        except Exception as e:
            print(f"Error checking URL {url}: {e}")

async def split_llm_response_and_tts(input_text: str, role: Role):
    stream_response = stream_answer(input_text, role_code=role.code)

        # 调用分段函数
    segments = segment_text(stream_response, segment_size=2)
    
    output_texts = ""
    _order = 0

    for segment in segments:
        output_texts += segment
        print(f"output_texts: {output_texts}")
        print(f"order: {_order}, tts_text: {segment}")

        tts_start_time = time.time()
        output_audio_path = await speak(segment, role.voice_type)
        tts_end_time = time.time()
        print(f"TTS succeed, output_audio_path: {output_audio_path}")
        print(f"TTS time cost: {tts_end_time-tts_start_time}, tts_start_time={tts_start_time}, tts_end_time={tts_end_time}")
        _order += 1
        result = {"url": get_audio_url(output_audio_path), "order": _order, "output_text": segment, "path": output_audio_path}
        yield result


    # output_texts = ""
    # _order = 0
    # for text in stream_response:
    #     output_texts += text
    #     print(f"output_texts: {output_texts}")
    #     split_texts = split_text(output_texts)
    #     print(f"split_texts: {split_texts}")
    #     for output_text in split_texts[_order:]:
    #         print(f"order: {_order}, tts_text: {output_text}")
    #         tts_start_time = time.time()
    #         output_audio_path = await speak(text=output_text, voice_type=role.voice_type)
    #         tts_end_time = time.time()
    #         print(f"TTS succeed, output_audio_path: {output_audio_path}")
    #         print(f"TTS time cost: {tts_end_time-tts_start_time}, tts_start_time={tts_start_time}, tts_end_time={tts_end_time}")
    #         _order += 1
    #         result = {"url": get_audio_url(output_audio_path), "order": _order, "output_text": output_text, "path": output_audio_path}
    #         yield result


def get_audio_url(path: str):
    file_name = get_audio_file_name(path)
    
    audio_url = config.audio_base_url + file_name
    
    return audio_url

def get_audio_file_name(path: str):
    file_name = path.split('/')[-1]
    return file_name


