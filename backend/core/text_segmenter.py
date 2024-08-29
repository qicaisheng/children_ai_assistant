import re
from typing import Generator

def split_text(text: str) -> list[str]:
    sentences = re.findall(r'.+?[。？！.?!]', text)
    if sentences:
        paragraphs = [sentences[0]]+ ["".join(sentences[i:i+2]) for i in range(1, len(sentences), 2)]
        return paragraphs
    
    return []


def segment_text(stream_response: Generator[str, None, None], segment_size=2) -> Generator[str, None, None]:
    """
    处理文本流，将其分段，每一段包含 segment_size 句。
    
    参数:
    - stream_response: 异步生成器，逐步返回文本片段。第一段是1句，后面每2句是一端。
    - segment_size: 每段包含的句子数量，默认为 2。

    返回:
    - 生成器，返回每一段分好的文本。
    """
    buffer = ""
    sentence_count = 0
    current_segment = ""
    
    for part in stream_response:
        buffer += part
        if buffer.strip().endswith(('.', '!', '?', "。", "！", "？")):
            sentence = buffer.strip()
            buffer = ""

            current_segment += " " + sentence if current_segment else sentence
            
            if sentence_count % segment_size == 0 or sentence_count == 0:
                yield current_segment
                current_segment = ""
            sentence_count += 1

    if current_segment:
        yield current_segment

