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
[]
    print(result)

generate_start_voices()
"""
{1: 'http://10.10.30.164:8082/voice-dc35fa1d919c4fbab1bba4ebcd391193.mp3', 2: 'http://10.10.30.164:8082/voice-0d5d1ed530c54ebd93bc0081fb4b4690.mp3', 3: 'http://10.10.30.164:8082/voice-144675ba17a14dcdb99acca61aec655a.mp3', 4: 'http://10.10.30.164:8082/voice-d5a84ad91deb41b7bebae0da70b0fb4e.mp3', 5: 'http://10.10.30.164:8082/voice-db753a1dff2a4c28b83cdfd7d8ae8fad.mp3'}
{1: 'http://10.10.30.164:8082/voice-765e83dc68d34cdbbb943e6682c5bab5.mp3', 2: 'http://10.10.30.164:8082/voice-cde2da13313c4e829a3f460a8cacb268.mp3', 3: 'http://10.10.30.164:8082/voice-b7c168237c75483389f7ee738b50b3b6.mp3', 4: 'http://10.10.30.164:8082/voice-783e492d3c7f4b7daf70585c130c7914.mp3', 5: 'http://10.10.30.164:8082/voice-16a57db36fe441babeb0174ee4b4edd1.mp3', 6: 'http://10.10.30.164:8082/voice-3ea36b642a9b41ecacd2a8aafe1a52d4.mp3', 7: 'http://10.10.30.164:8082/voice-7f0bffeab070435198610bff36084ed5.mp3'}
{1: 'http://10.10.30.164:8082/voice-99ee1632d0e142838107855c1de7eca8.mp3', 2: 'http://10.10.30.164:8082/voice-fee91558f66144259a0fb1d51999a5f4.mp3', 3: 'http://10.10.30.164:8082/voice-76b76efcc4c34e769421bb90c5f221d1.mp3', 4: 'http://10.10.30.164:8082/voice-efd1267b6f1948f68017cac9aaf8c1cd.mp3', 5: 'http://10.10.30.164:8082/voice-6ffbdc3a8f3640e2b177e0d07a2a7462.mp3', 6: 'http://10.10.30.164:8082/voice-ef5ec53ca3b64340b8a2d195021f4e5c.mp3', 7: 'http://10.10.30.164:8082/voice-396dba4bc8cf46749ba9909bcef2009d.mp3'}
"""

# generate_retry_voices()
"""
{1: 'http://10.10.30.164:8082/voice-0a570f047364438cb19cc2e425363c54.mp3', 2: 'http://10.10.30.164:8082/voice-278a3684b2ec4a339ec65786d4e53af2.mp3', 3: 'http://10.10.30.164:8082/voice-600625c59ca94b1ebb84f8b8e19d6724.mp3', 4: 'http://10.10.30.164:8082/voice-971ed17cbad148b1a9dc8a8cd51ea8fc.mp3', 5: 'http://10.10.30.164:8082/voice-78e0c93e6f0942bea7add2301c594a4f.mp3', 6: 'http://10.10.30.164:8082/voice-7ba3c1b253894af68b9e8769d301829c.mp3', 7: 'http://10.10.30.164:8082/voice-1843e12bca5d44fa8da6e0fba4092302.mp3'}
{1: 'http://10.10.30.164:8082/voice-cfccb70d0ef94d65814505f6f4752066.mp3', 2: 'http://10.10.30.164:8082/voice-53cb84cd16694454ac57e624b815ef84.mp3', 3: 'http://10.10.30.164:8082/voice-293f81f9ad4b4dada79e4132eae09bdf.mp3', 4: 'http://10.10.30.164:8082/voice-d32e9fe5344a4a2e875777c24123aa21.mp3', 5: 'http://10.10.30.164:8082/voice-c7383157fb684af697d0df69f1282eaf.mp3', 6: 'http://10.10.30.164:8082/voice-d30c4b8161d6422f9b529fab5e8076be.mp3', 7: 'http://10.10.30.164:8082/voice-7c1d1d305c8a47f581a4ba15a362c576.mp3'}

"""