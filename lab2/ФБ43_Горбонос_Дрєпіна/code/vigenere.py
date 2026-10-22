import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, RESULTS, ARTIFACTS = ROOT / "data", ROOT / "results", ROOT / "artifacts"
RESULTS.mkdir(exist_ok=True)
ARTIFACTS.mkdir(exist_ok=True)

A = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(A)
IDX = {c: i for i, c in enumerate(A)}

DEFAULT_FREQ = {
    "о": .1097, "е": .0849, "а": .0801, "и": .0735, "н": .0670, "т": .0626, "с": .0547, "р": .0473,
    "в": .0454, "л": .0440, "к": .0349, "м": .0321, "д": .0298, "п": .0281, "у": .0262, "я": .0201,
    "ы": .0190, "ь": .0174, "г": .0169, "з": .0164, "б": .0159, "ч": .0145, "й": .0121, "х": .0097,
    "ж": .0094, "ш": .0072, "ю": .0064, "ц": .0048, "щ": .0036, "э": .0033, "ф": .0026, "ъ": .0004,
}


def load_freq():
    path = DATA / "letter_freq_kp1.csv"
    if not path.exists():
        return dict(DEFAULT_FREQ)
    with open(path, encoding="utf-8") as f:
        freq = {row[0]: float(row[1]) for row in csv.reader(f) if row and row[0] in IDX}
    freq = {c: freq.get(c, DEFAULT_FREQ[c] if c == "ъ" else 0.0) for c in A}
    total = sum(freq.values())
    return {c: v / total for c, v in freq.items()}


FREQ = load_freq()


def prepare(text):
    return re.sub(r"[^а-я]", "", text.lower().replace("ё", "е"))


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return prepare(f.read())


def save_json(name, obj):
    with open(RESULTS / name, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def encrypt(x, key):
    return "".join(A[(IDX[c] + IDX[key[i % len(key)]]) % M] for i, c in enumerate(x))


def decrypt(y, key):
    return "".join(A[(IDX[c] - IDX[key[i % len(key)]]) % M] for i, c in enumerate(y))


def index_of_coincidence(s):
    n = len(s)
    if n < 2:
        return 0.0
    return sum(v * (v - 1) for v in Counter(s).values()) / (n * (n - 1))


def theoretical_index():
    return sum(p * p for p in FREQ.values())


def split_blocks(y, r):
    return [y[i::r] for i in range(r)]


def avg_block_ic(y, r):
    return sum(index_of_coincidence(b) for b in split_blocks(y, r)) / r


def coincidences(y, r):
    return sum(1 for i in range(len(y) - r) if y[i] == y[i + r])


def shift_by_letter(block, letter="о"):
    ystar = Counter(block).most_common(1)[0][0]
    return (IDX[ystar] - IDX[letter]) % M


def shift_by_freq(block):
    cnt, n = Counter(block), len(block)
    score = lambda k: sum(FREQ[A[t]] * cnt.get(A[(t + k) % M], 0) / n for t in range(M))
    return max(range(M), key=score)


def recover_key(y, r):
    return "".join(A[shift_by_freq(b)] for b in split_blocks(y, r))
