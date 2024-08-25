import asyncio
from service.audio_service import get_audio_url
from core.role import roles, Role
from service.tts_websocket_demo import speak

def generate_start_voices():
    result = {}
    for role_dict in roles:
        role = Role(**role_dict)
        loop = asyncio.get_event_loop()
        audio_path = loop.run_until_complete(speak(role.self_introduction, role.voice_type))
        url=get_audio_url(audio_path)
        result[role.code] = url

    print(result)

# generate_start_voices()

"""
{1: 'http://10.10.30.164:8082/voice-dc35fa1d919c4fbab1bba4ebcd391193.mp3', 2: 'http://10.10.30.164:8082/voice-0d5d1ed530c54ebd93bc0081fb4b4690.mp3', 3: 'http://10.10.30.164:8082/voice-144675ba17a14dcdb99acca61aec655a.mp3', 4: 'http://10.10.30.164:8082/voice-d5a84ad91deb41b7bebae0da70b0fb4e.mp3', 5: 'http://10.10.30.164:8082/voice-db753a1dff2a4c28b83cdfd7d8ae8fad.mp3'}
"""
        