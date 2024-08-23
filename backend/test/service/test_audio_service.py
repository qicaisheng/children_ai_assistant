import service.audio_service as audio_service

def test_get_audio_url(monkeypatch):
    monkeypatch.setattr('config.audio_base_url', "http://localhost:8082/")
    
    audio_url = audio_service.get_audio_url("../audio/recording-042a907e-2342-4935-8af2-374fbdb419cb.wav")
    
    assert audio_url == "http://localhost:8082/recording-042a907e-2342-4935-8af2-374fbdb419cb.wav"
