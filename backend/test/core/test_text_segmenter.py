from core.text_segmenter import split_text


def test_split_text():
    text = "这是第一句。这是第二句！这是第三句？这是第四句。这是第五句！这是第六句?这是第七句！"
    result = split_text(text)

    assert len(result) == 4
    assert result[0] == "这是第一句。这是第二句！"
    assert result[1] == "这是第三句？这是第四句。"
    assert result[2] == "这是第五句！这是第六句?"
    assert result[3] == "这是第七句！"
    