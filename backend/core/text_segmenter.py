import re

def split_text(text: str) -> list[str]:
    sentences = re.findall(r'.+?[。？！.?!]', text)
    if sentences:
        paragraphs = [sentences[0]]+ ["".join(sentences[i:i+2]) for i in range(1, len(sentences), 2)]
        return paragraphs
    
    return []
