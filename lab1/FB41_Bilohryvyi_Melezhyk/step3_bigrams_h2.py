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


def entropy_from_counts(counts: Counter, total: int) -> float:
    h = 0.0
    for c in counts.values():
        p = c / total
        h -= p * math.log2(p)
    return h


def bigrams_overlapping(text: str):
    # (x1x2),(x2x3),(x3x4)... зміщення на 1 символ
    return [text[i:i + 2] for i in range(len(text) - 1)]


def bigrams_nonoverlapping(text: str):
    # (x1x2),(x3x4)... зміщення на 2 символи
    return [text[i:i + 2] for i in range(0, len(text) - 1, 2)]


def h2_per_symbol(bigram_list) -> float:
    counts = Counter(bigram_list)
    total = sum(counts.values())
    h_joint = entropy_from_counts(counts, total)
    return h_joint / 2.0   # ділимо на 2, бо H2 має бути "на символ", а не "на біграму"


raw = open("voina_i_mir.txt", encoding="utf-8", errors="ignore").read()
text_with_spaces = preprocess(raw, keep_spaces=True)
text_no_spaces = preprocess(raw, keep_spaces=False)

for label, text in [("з пробілами", text_with_spaces), ("без пробілів", text_no_spaces)]:
    bg_over = bigrams_overlapping(text)
    bg_nonover = bigrams_nonoverlapping(text)

    h2_over = h2_per_symbol(bg_over)
    h2_nonover = h2_per_symbol(bg_nonover)

    print(f"\n=== {label} ===")
    print(f"Кількість перекривних біграм: {len(bg_over)}")
    print(f"Кількість неперекривних біграм: {len(bg_nonover)}")
    print(f"H2 (перекривні)    = {h2_over:.4f} біт/символ")
    print(f"H2 (неперекривні)  = {h2_nonover:.4f} біт/символ")

    print("Топ-5 біграм (перекривні):")
    for bg, n in Counter(bg_over).most_common(5):
        display = bg.replace(" ", "␣")
        print(f"  '{display}': {n}")