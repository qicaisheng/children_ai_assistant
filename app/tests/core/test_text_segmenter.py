from typing import Generator
from app.core.text_segmenter import segment_text, split_text


def test_split_text():
    text = "这是第一句"
    result = split_text(text)
    assert len(result) == 0

    text = "这是第一句。"
    result = split_text(text)
    assert len(result) == 1
    assert result[0] ==  "这是第一句。"


    text = "这是第一句。这是第二句！这是第三句？这是第四句。这是第五句！这是第六句?这是第七句！"
    result = split_text(text)

    assert len(result) == 4
    assert result[0] == "这是第一句。"
    assert result[1] == "这是第二句！这是第三句？"
    assert result[2] == "这是第四句。这是第五句！"
    assert result[3] == "这是第六句?这是第七句！"

    text = "这是第一句。这是第二句！这是第三句？这是第四句。这是第五句！这是第六句?这是第七句！这是第八句！"
    result = split_text(text)

    assert len(result) == 5
    assert result[0] == "这是第一句。"
    assert result[1] == "这是第二句！这是第三句？"
    assert result[2] == "这是第四句。这是第五句！"
    assert result[3] == "这是第六句?这是第七句！"
    assert result[4] == "这是第八句！"
    

def simulate_stream_response(text: str) -> Generator[str, None, None]:
    """
    模拟按字生成的 stream_response 生成器。
    """
    for char in text:
        yield char

def test_single_sentence():
    stream = simulate_stream_response("This is a sentence.")
    result = list(segment_text(stream))
    assert result == ["This is a sentence."]
    
def test_two_sentences():
    stream = simulate_stream_response("This is the first sentence. This is the second sentence.")
    result = list(segment_text(stream))
    assert result == ["This is the first sentence.", "This is the second sentence."]
    
def test_three_sentences():
    stream = simulate_stream_response("This is the first sentence. This is the second sentence. This is the third sentence.")
    result = list(segment_text(stream, segment_size=2))
    print(result)
    assert result == ["This is the first sentence.", "This is the second sentence. This is the third sentence."]
    
def test_multiple_sentences():
    stream = simulate_stream_response(
        "This is the first sentence. This is the second sentence. This is the third sentence. This is the fourth sentence."
    )
    result = list(segment_text(stream, segment_size=2))
    assert result == [
        "This is the first sentence.",
        "This is the second sentence. This is the third sentence.",
        "This is the fourth sentence."
    ]

def test_chinese_sentences():
    stream = simulate_stream_response("这是第一句。这是第二句。这是第三句。这是第四句。")
    result = list(segment_text(stream, segment_size=2))
    assert result == [
        "这是第一句。",
        "这是第二句。 这是第三句。",
        "这是第四句。"
    ]

def test_incomplete_last_segment():
    stream = simulate_stream_response("This is the first sentence. This is the second sentence. This is the third sentence.")
    result = list(segment_text(stream, segment_size=2))
    assert result == ["This is the first sentence.", "This is the second sentence. This is the third sentence."]

def test_tts_spliter_flag_false(monkeypatch):
    monkeypatch.setattr("config.tts_spliter_flag", False)
    
    stream = simulate_stream_response("This is the first sentence. This is the second sentence. This is the third sentence.")
    result = list(segment_text(stream, segment_size=2))
    assert result == ["This is the first sentence. This is the second sentence. This is the third sentence."]