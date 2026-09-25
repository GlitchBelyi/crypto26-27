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


def entropy_from_counts(counts: Counter, total: int) -> float:
    h = 0.0
    for c in counts.values():
        p = c / total
        h -= p * math.log2(p)
    return h


def bigrams_overlapping(text):
    return [text[i:i + 2] for i in range(len(text) - 1)]


def bigrams_nonoverlapping(text):
    return [text[i:i + 2] for i in range(0, len(text) - 1, 2)]


def h2_per_symbol(bigram_list):
    counts = Counter(bigram_list)
    total = sum(counts.values())
    return entropy_from_counts(counts, total) / 2.0


raw = open("voina_i_mir.txt", encoding="utf-8", errors="ignore").read()
text_no_spaces = preprocess(raw, keep_spaces=False)

LENGTH = 20000
SEED = 42
rng = random.Random(SEED)

base = text_no_spaces[:LENGTH]

chars_G = list(base)
rng.shuffle(chars_G)
seq_G = "".join(chars_G)

counts = Counter(base)
symbols_sorted = sorted(counts.keys())
remaining = dict(counts)
pattern = []
while sum(remaining.values()) > 0:
    for s in symbols_sorted:
        if remaining.get(s, 0) > 0:
            pattern.append(s)
            remaining[s] -= 1
seq_D = "".join(pattern)

for name, seq in [("G", seq_G), ("D", seq_D)]:
    c = Counter(seq)
    h1 = entropy_from_counts(c, len(seq))
    h2_over = h2_per_symbol(bigrams_overlapping(seq))
    h2_nonover = h2_per_symbol(bigrams_nonoverlapping(seq))
    print(f"\nПослідовність {name}: довжина={len(seq)}")
    print(f"  H1 = {h1:.4f}")
    print(f"  H2 (перекривні)   = {h2_over:.4f}")
    print(f"  H2 (неперекривні) = {h2_nonover:.4f}")