import math
import random
from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_SPACE = ALPHABET + " "
CORPUS_PATH = "corpus.txt"


def normalize(text, alphabet):
    text = text.lower().replace("ё", "е")
    allowed = set(alphabet)
    text = "".join(ch if ch in allowed else " " for ch in text)
    return " ".join(text.split())


def freqs(text):
    return Counter(text)


def bigrams(text, overlap):
    step = 1 if overlap else 2
    return Counter(text[i:i + 2] for i in range(0, len(text) - 1, step))


def top5(counter):
    total = sum(counter.values())
    return [(s, c, c / total) for s, c in counter.most_common(5)]


def entropy(counter):
    total = sum(counter.values())
    return -sum(
        (c / total) * math.log2(c / total)
        for c in counter.values()
        if c
    ) + 0.0


def h1(text):
    return entropy(freqs(text))


def h2(text, overlap):
    return entropy(bigrams(text, overlap)) / 2


def redundancy(h, m):
    return 1 - h / math.log2(m)


def seq_repeat(symbol, length):
    return symbol * length


def seq_random_uniform(alphabet, length, seed):
    rng = random.Random(seed)
    return "".join(rng.choice(alphabet) for _ in range(length))


def seq_shuffled(text, seed):
    rng = random.Random(seed)
    pool = list(text)
    rng.shuffle(pool)
    return "".join(pool)


def seq_periodic(a, b, length):
    reps = length // 2 + 1
    return ((a + b) * reps)[:length]


out = []


def w(s=""):
    out.append(s)
    print(s)


def w_top5(rows):
    for item, cnt, frac in rows:
        label = "пробіл" if item == " " else item
        w(f"    {label!r:>10}   {cnt:>8}   {frac:.4f}")


with open(CORPUS_PATH, encoding="utf-8") as f:
    raw = f.read()

text_space = normalize(raw, ALPHABET_SPACE)
text_nospace = text_space.replace(" ", "")

w("=" * 60)
w("ДОВЖИНА ТЕКСТУ")
w("=" * 60)
w(f"символів до нормалізації : {len(raw)}")
w(f"символів з пробілами     : {len(text_space)}")
w(f"символів без пробілів    : {len(text_nospace)}")
w()

for label, text, alphabet in [
    ("ТЕКСТ З ПРОБІЛОМ", text_space, ALPHABET_SPACE),
    ("ТЕКСТ БЕЗ ПРОБІЛІВ", text_nospace, ALPHABET),
]:
    w("=" * 60)
    w(f"{label} (алфавіт із {len(alphabet)} символів)")
    w("=" * 60)

    w("Топ-5 символів (символ, кількість, частка):")
    w_top5(top5(freqs(text)))

    w("Топ-5 біграм, що ПЕРЕТИНАЮТЬСЯ:")
    w_top5(top5(bigrams(text, True)))

    w("Топ-5 біграм, що НЕ перетинаються:")
    w_top5(top5(bigrams(text, False)))

    w(f"H1              = {h1(text):.4f} біт/симв.")
    w(f"H2 (перетин.)   = {h2(text, True):.4f} біт/симв.")
    w(f"H2 (без перет.) = {h2(text, False):.4f} біт/симв.")
    w()


# ПОСЛІДОВНОСТІ А, Б, В

seq_len = min(20000, len(text_nospace))

A = text_nospace[:seq_len]

B = seq_repeat("о", seq_len)

V = seq_random_uniform(
    ALPHABET,
    seq_len,
    seed=1
)

w("=" * 60)
w(f"ПОСЛІДОВНОСТІ А, Б, В (довжина {seq_len})")
w("=" * 60)

w(f"H1(А, фрагмент природного тексту) = {h1(A):.4f}")
w(f"H1(Б, повторення символу «о»)     = {h1(B):.4f}")
w(f"H1(В, рівноімовірна випадкова)    = {h1(V):.4f}")
w()


# ПОСЛІДОВНОСТІ Г, Д

# Беремо дві найчастіші літери тексту
top2 = [s for s, _ in Counter(text_nospace).most_common(2)]

a = top2[0]
b = top2[1]

# Створюємо базову послідовність:
# половина символів a, половина символів b.
# Таким чином Г і Д матимуть однакові частоти символів.

base = (
    a * (seq_len // 2)
    + b * (seq_len - seq_len // 2)
)

# Г — ті самі символи, але у випадковому порядку
G = seq_shuffled(base, seed=2)

# Д — ті самі символи і ті самі частоти,
# але у строгій періодичній структурі abab...
D = seq_periodic(a, b, seq_len)


w("=" * 60)
w(f"ПОСЛІДОВНОСТІ Г, Д (довжина {seq_len})")
w("=" * 60)

w(f"Використані символи: «{a}» та «{b}»")
w()

w(f"H1(Г)              = {h1(G):.4f}")
w(f"H1(Д)              = {h1(D):.4f}")

w(f"H2(Г, перетин.)    = {h2(G, True):.4f}")
w(f"H2(Г, без перет.)  = {h2(G, False):.4f}")

w(f"H2(Д, перетин.)    = {h2(D, True):.4f}")
w(f"H2(Д, без перет.)  = {h2(D, False):.4f}")

w()


# НАДЛИШКОВІСТЬ

m = len(ALPHABET)

w("=" * 60)
w("НАДЛИШКОВІСТЬ (текст без пробілів)")
w("=" * 60)

w(f"R(H1) = {redundancy(h1(text_nospace), m):.4f}")
w(f"R(H2) = {redundancy(h2(text_nospace, True), m):.4f}")


# ЗАПИС РЕЗУЛЬТАТІВ У ФАЙЛ

with open("results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))