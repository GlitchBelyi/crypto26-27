import math
import random
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


def entropy_H1(counts: Counter, total: int) -> float:
    h = 0.0
    for c in counts.values():
        p = c / total
        h -= p * math.log2(p)
    return h


raw = open("voina_i_mir.txt", encoding="utf-8", errors="ignore").read()
text_no_spaces = preprocess(raw, keep_spaces=False)

LENGTH = 20000
SEED = 42
rng = random.Random(SEED)

# А — фрагмент природного тексту
seq_A = text_no_spaces[:LENGTH]

# Б — повторення одного символу (беремо найчастіший символ джерела)
most_common_char = Counter(text_no_spaces).most_common(1)[0][0]
seq_B = most_common_char * LENGTH

# В — випадкова рівноймовірна послідовність з того самого алфавіту
alphabet = sorted(set(text_no_spaces))
seq_V = "".join(rng.choice(alphabet) for _ in range(LENGTH))

print(f"Алфавіт джерела: {len(alphabet)} символів")
print(f"Найчастіший символ (для Б): '{most_common_char}'")

for name, seq in [("A", seq_A), ("B", seq_B), ("V", seq_V)]:
    counts = Counter(seq)
    h1 = entropy_H1(counts, len(seq))
    print(f"\nПослідовність {name}: довжина={len(seq)}, "
          f"унікальних символів={len(counts)}, H1={h1:.4f} біт/символ")