import re

RUSSIAN_LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_WITH_SPACE = set(RUSSIAN_LETTERS + " ")


def preprocess(raw_text: str, keep_spaces: bool = True) -> str:
    text = raw_text.lower()
    text = text.replace("ё", "е")

    text = "".join(ch if ch in ALPHABET_WITH_SPACE else " " for ch in text)

    text = re.sub(r" +", " ", text).strip()

    if not keep_spaces:
        text = text.replace(" ", "")

    return text


raw = open("voina_i_mir.txt", encoding="utf-8", errors="ignore").read()

text_with_spaces = preprocess(raw, keep_spaces=True)
text_no_spaces = preprocess(raw, keep_spaces=False)

print("Довжина сирого тексту:", len(raw))
print("Довжина після нормалізації (з пробілами):", len(text_with_spaces))
print("Довжина без пробілів:", len(text_no_spaces))
print("Перші 300 символів після обробки:")
print(text_with_spaces[:300])

