import math
import random
from collections import Counter

RUSSIAN_ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"  # 32 літери (ё -> е)
ALPHABET_WITH_SPACE = RUSSIAN_ALPHABET + " "


# 1. Попередня обробка тексту

def normalize_text(raw_text: str, alphabet: str = RUSSIAN_ALPHABET) -> str:
    
    text = raw_text.lower().replace("ё", "е")
    allowed = set(alphabet)
    out_chars = []
    for ch in text:
        out_chars.append(ch if ch in allowed else " ")
    collapsed = " ".join("".join(out_chars).split())
    return collapsed


def remove_spaces(text: str) -> str:
    return text.replace(" ", "")


# 2. Частоти символів і n-грам

def symbol_frequencies(text: str) -> Counter:
    return Counter(text)


def bigram_frequencies(text: str, overlapping: bool = True) -> Counter:
    step = 1 if overlapping else 2
    bigrams = (text[i:i + 2] for i in range(0, len(text) - 1, step))
    return Counter(b for b in bigrams if len(b) == 2)


def top_n(counter: Counter, n: int = 5):
    total = sum(counter.values())
    return [(item, cnt, cnt / total) for item, cnt in counter.most_common(n)]


# 3. Ентропія

def entropy_from_counts(counter: Counter) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    h = 0.0
    for cnt in counter.values():
        p = cnt / total
        if p > 0:
            h -= p * math.log2(p)
    return h


def h1(text: str) -> float:
    return entropy_from_counts(symbol_frequencies(text))


def h2_per_symbol(text: str, overlapping: bool = True) -> float:
    """
     Ділимо на 2, щоб
    порівнювати H1 і H2 в одних одиницях (біт/символ).
    """
    bigrams = bigram_frequencies(text, overlapping=overlapping)
    return entropy_from_counts(bigrams) / 2


# 4. Штучні послідовності для розділів 3 і 4 методички

def make_sequence_B(symbol: str, length: int) -> str:
    """Б — повторення одного символу."""
    return symbol * length


def make_sequence_V(alphabet: str, length: int, seed: int = 1) -> str:
    """В — рівноімовірна випадкова послідовність символів алфавіту."""
    rng = random.Random(seed)
    return "".join(rng.choice(alphabet) for _ in range(length))


def make_sequence_G(text_for_freqs: str, length: int, seed: int = 2) -> str:
    """
    Г — символи в випадковому порядку, але з частотами, близькими до
    частот природного тексту (перемішування символів природного фрагмента).
    """
    rng = random.Random(seed)
    pool = list(text_for_freqs[:length]) if len(text_for_freqs) >= length else \
        list((text_for_freqs * (length // len(text_for_freqs) + 1))[:length])
    rng.shuffle(pool)
    return "".join(pool)


def make_sequence_D(two_symbols: str, length: int) -> str:
    """Д — виражена періодична структура: abababab..."""
    a, b = two_symbols[0], two_symbols[1]
    pattern = a + b
    reps = length // 2 + 1
    return (pattern * reps)[:length]


# 5. Надлишковість

def redundancy(h_inf: float, alphabet_size: int) -> float:
    h0 = math.log2(alphabet_size)
    return 1 - h_inf / h0