import math
import re
import random
from collections import Counter

CUSTOM_ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыюя"
ALLOWED_CHARS = set(CUSTOM_ALPHABET + " ")
ALPHABET_LIST = list(ALLOWED_CHARS)

def clean_text(raw_data: str, keep_spaces: bool = True) -> str:
    text = raw_data.lower()
    replacements = {"ё": "е", "ъ": "ь", "э": "е"}
    for old_char, new_char in replacements.items():
        text = text.replace(old_char, new_char)
    filtered_chars = [ch if ch in ALLOWED_CHARS else " " for ch in text]
    text = "".join(filtered_chars)
    text = re.sub(r"\s+", " ", text).strip()
    if not keep_spaces:
        text = text.replace(" ", "")
    return text

def compute_entropy(counts: Counter, total: int) -> float:
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def compute_entropy_h1(text: str) -> float:
    counts = Counter(text)
    return compute_entropy(counts, len(text))


def task3(natural_text: str, n: int, seed: int = 42):
    random.seed(seed)

    # А — фрагмент природного тексту (випадковий зсув у межах файлу)
    start = random.randint(0, max(0, len(natural_text) - n - 1))
    seq_A = natural_text[start:start + n]

    # Б — повторення одного символу 
    most_common_char = Counter(natural_text).most_common(1)[0][0]
    seq_B = most_common_char * n

    # В — випадкова рівноймовірна послідовність
    seq_V = "".join(random.choices(ALPHABET_LIST, k=n))

    print(f"{'Послідовність':35s} {'H1 (біт/символ)':>18s}")
    print("-" * 55)
    for name, seq in [("А (природний текст)", seq_A),
                       ("Б (один символ, повтор)", seq_B),
                       ("В (рівноймовірний випадковий)", seq_V)]:
        h1 = compute_entropy_h1(seq)
        print(f"{name:35s} {h1:18.5f}")

    max_h0 = math.log2(len(ALPHABET_LIST))
    print(f"\nДовідково: |алфавіт| = {len(ALPHABET_LIST)}, H0 (максимум) = {max_h0:.5f} біт/символ")


if __name__ == "__main__":
    filename = "Pyat_lojek_eliksira.txt"   
    N = 100000

    with open(filename, encoding="utf-8", errors="ignore") as f:
        raw = f.read()    

    natural = clean_text(raw, keep_spaces=True)
    task3(natural, N)