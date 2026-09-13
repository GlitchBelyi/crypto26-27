import math
import re
from collections import Counter

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


def char_frequencies(text: str) -> Counter:
    return Counter(text)


def entropy_H1(counts: Counter, total: int) -> float:
    h = 0.0
    for c in counts.values():
        p = c / total
        h -= p * math.log2(p)
    return h


# --- читаємо і обробляємо текст ---
raw = open("voina_i_mir.txt", encoding="utf-8", errors="ignore").read()
text_with_spaces = preprocess(raw, keep_spaces=True)
text_no_spaces = preprocess(raw, keep_spaces=False)

for label, text in [("з пробілами", text_with_spaces), ("без пробілів", text_no_spaces)]:
    counts = char_frequencies(text)
    total = len(text)
    h1 = entropy_H1(counts, total)

    print(f"\n=== {label} ===")
    print(f"Довжина тексту: {total}")
    print(f"Розмір алфавіту (унікальних символів): {len(counts)}")
    print(f"H1 = {h1:.4f} біт/символ")

    print("Топ-5 символів за частотою:")
    for ch, n in counts.most_common(5):
        symbol = "␣ (пробіл)" if ch == " " else ch
        p = n / total
        print(f"  {symbol}: кількість={n}, ймовірність={p:.4f}")