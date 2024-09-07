from core.role import get_current_role
import service.audio_service as audio_service
import asyncio

def test_get_audio_url(monkeypatch):
    monkeypatch.setattr('config.audio_base_url', "http://localhost:8082/")
    
    audio_url = audio_service.get_audio_url("../audio/recording-042a907e-2342-4935-8af2-374fbdb419cb.wav")
    
    assert audio_url == "http://localhost:8082/recording-042a907e-2342-4935-8af2-374fbdb419cb.wav"


loop = asyncio.get_event_loop()
loop.run_until_complete(audio_service.process_user_input_text(audio_path="../audio/input-voice.wav", recording_id=1, role=get_current_role(), input_text="hello"))
