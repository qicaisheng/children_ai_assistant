from service.tts.tts import TTS
from service.asr.asr import ASR

# host = "10.10.30.164"
host = "localhost"
audio_base_url = f"http://{host}:8082/"
audio_file_direction = "../audio"
udp_host = host
udp_port = 8085
mqtt_host = host
mqtt_port = 1883

tts = TTS.VOLCENGINE
asr = ASR.VOLCENGINE