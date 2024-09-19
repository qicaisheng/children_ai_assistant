from app.core.story import Story, get_story_by_name

def test_get_story_by_name(monkeypatch):
    monkeypatch.setattr("app.config.audio_base_url", "http://localhost:8082/")

    story = get_story_by_name("走失的小野雁")

    expected_story = {
        "name": "走失的小野雁",
        "audio_ids": ["走失的小野雁.mp3"],
        "season": 1,
        "episode": "5A"
    }

    assert story == Story(**expected_story)
    assert story.get_audio_urls() == ["http://localhost:8082/走失的小野雁.mp3"]
