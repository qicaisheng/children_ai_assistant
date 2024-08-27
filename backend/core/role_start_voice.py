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

def generate_retry_voices():
    text = "不好意思，没听清楚，可以再说一遍吗"
    result = {}
    for role_dict in roles:
        role = Role(**role_dict)
        loop = asyncio.get_event_loop()
        audio_path = loop.run_until_complete(speak(text, role.voice_type))
        url=get_audio_url(audio_path)
        result[role.code] = url

    print(result)

# generate_start_voices()
"""
{1: 'http://10.10.30.164:8082/voice-dc35fa1d919c4fbab1bba4ebcd391193.mp3', 2: 'http://10.10.30.164:8082/voice-0d5d1ed530c54ebd93bc0081fb4b4690.mp3', 3: 'http://10.10.30.164:8082/voice-144675ba17a14dcdb99acca61aec655a.mp3', 4: 'http://10.10.30.164:8082/voice-d5a84ad91deb41b7bebae0da70b0fb4e.mp3', 5: 'http://10.10.30.164:8082/voice-db753a1dff2a4c28b83cdfd7d8ae8fad.mp3'}
"""

generate_retry_voices()
"""
{1: 'http://10.10.30.164:8082/voice-0a570f047364438cb19cc2e425363c54.mp3', 2: 'http://10.10.30.164:8082/voice-278a3684b2ec4a339ec65786d4e53af2.mp3', 3: 'http://10.10.30.164:8082/voice-600625c59ca94b1ebb84f8b8e19d6724.mp3', 4: 'http://10.10.30.164:8082/voice-971ed17cbad148b1a9dc8a8cd51ea8fc.mp3', 5: 'http://10.10.30.164:8082/voice-78e0c93e6f0942bea7add2301c594a4f.mp3', 6: 'http://10.10.30.164:8082/voice-7ba3c1b253894af68b9e8769d301829c.mp3', 7: 'http://10.10.30.164:8082/voice-1843e12bca5d44fa8da6e0fba4092302.mp3'}"""