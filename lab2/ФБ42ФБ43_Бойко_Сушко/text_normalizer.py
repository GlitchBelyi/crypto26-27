import re

CLEAN_PATTERN = re.compile(r'[^а-я]+')

def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace('ё', 'е')
    text = CLEAN_PATTERN.sub('', text)
    return text

with open('Task1_plain.txt', 'r', encoding='utf-8') as f:
    text = f.read()

normalized = normalize_text(text)

with open('Task1_normalized.txt', 'w', encoding='utf-8') as f:
    f.write(normalized)