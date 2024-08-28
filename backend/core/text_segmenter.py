import re

def split_text(text: str) -> list[str]:
    sentences = re.findall(r'.+?[。？！.?!]', text)
    if sentences:
        paragraphs = [sentences[0]]+ ["".join(sentences[i:i+2]) for i in range(1, len(sentences), 2)]
        return paragraphs
    
    return []


# text_segmenter.py

def segment_text(stream_response, segment_size=2):
    """
    处理文本流，将其分段，每一段包含 segment_size 句。
    
    参数:
    - stream_response: 异步生成器，逐步返回文本片段。
    - segment_size: 每段包含的句子数量，默认为 2。

    返回:
    - 生成器，返回每一段分好的文本。
    """
    buffer = ""
    sentence_count = 0
    current_segment = ""
    
    for part in stream_response:
        buffer += part
        # 检查是否为完整句子结束
        if buffer.strip().endswith(('.', '!', '?', "。", "！", "？")):
            sentence = buffer.strip()
            buffer = ""  # 清空缓冲区
            
            if sentence_count == 0:
                # 第一段只包含第一个完整句子
                current_segment = sentence
                yield current_segment
                current_segment = ""
            else:
                # 后面的每 segment_size 句作为一段
                if sentence_count % segment_size == 0:
                    if current_segment:
                        yield current_segment
                    current_segment = sentence
                else:
                    current_segment += " " + sentence

            sentence_count += 1
    
    # 将最后未处理的段落处理掉
    if current_segment:
        yield current_segment

