import re

RUSSIAN_LETTERS = "абвгдежзийклмнопрстуфхцчшщыьюя"
ALPHABET_WITH_SPACE = set(RUSSIAN_LETTERS + " ")

def preprocess(raw_text: str, keep_spaces: bool = True) -> str:
    text = raw_text.lower()
    text = text.replace("ё", "е")
    text = text.replace("ъ", "ь") 
    text = text.replace("э", "е")
    text = "".join(ch if ch in ALPHABET_WITH_SPACE else " " for ch in text)
    text = re.sub(r" +", " ", text).strip()

    if not keep_spaces:
        text = text.replace(" ", "")    
    return text

filename = "Pyat_lojek_eliksira.txt"

try:
    with open(filename, encoding="utf-8", errors="ignore") as file:
        raw = file.read()

    text_with_spaces = preprocess(raw, keep_spaces=True)
    text_no_spaces = preprocess(raw, keep_spaces=False)

    print(f"Довжина сирого тексту: {len(raw)}")
    print(f"Довжина після нормалізації (з пробілами): {len(text_with_spaces)}")
    print(f"Довжина без пробілів: {len(text_no_spaces)}") 
    print("\nПерші 300 символів після обробки (з пробілами):")
    print(text_with_spaces[:300])   
except FileNotFoundError:
    print(f"Помилка: Файл '{filename}' не знайдено. Переконайтеся, що він лежить у тій самій папці, що й скрипт.")
    