import json
import os
import re
from collections import Counter
 
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}
_DEFAULT_FREQ = {
    "о": 0.11388, "е": 0.08916, "а": 0.07707, "и": 0.06769, "т": 0.06588,
    "н": 0.06152, "с": 0.05298, "в": 0.04658, "л": 0.04510, "р": 0.04064,
    "м": 0.03332, "к": 0.03265, "д": 0.03176, "у": 0.02899, "п": 0.02658,
    "я": 0.02071, "ь": 0.02069, "г": 0.01928, "б": 0.01812, "ч": 0.01797,
    "ы": 0.01680, "з": 0.01537, "ж": 0.01115, "й": 0.01009, "ш": 0.00969,
    "х": 0.00770, "ю": 0.00683, "э": 0.00363, "ц": 0.00339, "щ": 0.00286,
    "ф": 0.00171, "ъ": 0.00024,
}
def load_freq():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "freq_ru.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            freq = json.load(f)
    else:
        freq = dict(_DEFAULT_FREQ)
    s = sum(freq.values())
    return {c: freq.get(c, 0.0) / s for c in ALPHABET} 
FREQ = load_freq()
FREQ_ORDER = sorted(ALPHABET, key=lambda c: -FREQ[c])   
I_LANG = sum(p * p for p in FREQ.values())               
I_RANDOM = 1.0 / M                                        
def clean(text):
    text = text.lower().replace("ё", "е")
    return re.sub("[^" + ALPHABET + "]", "", text)

def vigenere(text, key, decrypt=False):
    sign = -1 if decrypt else 1
    k = [IDX[c] for c in key]
    r = len(k)
    return "".join(ALPHABET[(IDX[c] + sign * k[i % r]) % M] for i, c in enumerate(text))
def encrypt(text, key):
    return vigenere(text, key, False)
def decrypt(text, key):
    return vigenere(text, key, True)

def index_of_coincidence(text):
    n = len(text)
    if n < 2:
        return 0.0
    return sum(c * (c - 1) for c in Counter(text).values()) / (n * (n - 1))
def blocks(text, r):
    return [text[i::r] for i in range(r)]
def avg_block_ic(text, r):
    bl = blocks(text, r)
    return sum(index_of_coincidence(b) for b in bl) / r
def d_stat(text, r):
    """D_r = sum_i delta(y_i, y_{i+r})."""
    return sum(1 for i in range(len(text) - r) if text[i] == text[i + r])
def read_cipher(path, variant):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    parts = re.split(r"Вариант\s+(\d+)", t)
    d = {int(parts[i]): clean(parts[i + 1]) for i in range(1, len(parts), 2)}
    return d[variant]