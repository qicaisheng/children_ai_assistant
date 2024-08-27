import re

def split_text(text: str) -> list[str]:
    sentences = re.findall(r'.+?[。？！.?!]', text)
    
    paragraphs = ["".join(sentences[i:i+2]) for i in range(0, len(sentences), 2)]
    
    return paragraphs
