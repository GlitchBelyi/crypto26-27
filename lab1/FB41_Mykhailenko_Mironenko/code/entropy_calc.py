from collections import Counter
from math import log2


def entropy(counter):
    total = sum(counter.values())

    if total == 0:
        return 0.0

    result = 0.0

    for count in counter.values():
        p = count / total
        result -= p * log2(p)

    return result


def bigrams(text, step):
    return Counter(
        text[i:i + 2]
        for i in range(0, len(text) - 1, step)
    )


def h1(text):
    return entropy(Counter(text))


def h2(text, step):
    return entropy(bigrams(text, step)) / 2


def analyze_text(text, alphabet_size):
    chars = Counter(text)
    overlap = bigrams(text, 1)
    nonoverlap = bigrams(text, 2)

    h0 = log2(alphabet_size)
    value_h1 = entropy(chars)
    value_h2_overlap = entropy(overlap) / 2
    value_h2_nonoverlap = entropy(nonoverlap) / 2

    return {
        "length": len(text),
        "H0": h0,
        "H1": value_h1,
        "H2_overlap": value_h2_overlap,
        "H2_nonoverlap": value_h2_nonoverlap,
        "characters": chars,
        "bigrams_overlap": overlap,
        "bigrams_nonoverlap": nonoverlap,
    }


def redundancy(h, h0):
    return 1 - h / h0


def top5(counter):
    total = sum(counter.values())

    return [
        (symbol, count, count / total)
        for symbol, count in counter.most_common(5)
    ]