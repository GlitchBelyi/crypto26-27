import csv
from collections import Counter
from math import log2
from pathlib import Path

DATA_DIR = Path("data")
OUT_DIR = Path("results")
TEXTS = {
    "with_spaces": DATA_DIR / "text_with_spaces.txt",
    "no_spaces": DATA_DIR / "text_no_spaces.txt",
}


def entropy(counter):
    total = sum(counter.values())
    return -sum(c / total * log2(c / total) for c in counter.values()) + 0.0


def ngrams(text, n, step):
    return Counter(text[i:i + n] for i in range(0, len(text) - n + 1, step))


def show(symbol):
    return "_" if symbol == " " else symbol.replace(" ", "_")


def save_table(path, counter, header):
    total = sum(counter.values())
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for symbol, count in counter.most_common():
            writer.writerow([show(symbol), count, f"{count / total:.6f}"])


def top(counter, k=5):
    total = sum(counter.values())
    return ", ".join(f"'{show(s)}': {c} ({c / total:.4f})" for s, c in counter.most_common(k))


def main():
    OUT_DIR.mkdir(exist_ok=True)
    for name, path in TEXTS.items():
        text = path.read_text(encoding="utf-8")
        chars = ngrams(text, 1, 1)
        bi_over = ngrams(text, 2, 1)
        bi_disj = ngrams(text, 2, 2)
        m = len(chars)
        h0 = log2(m)
        h1 = entropy(chars)
        h2_over = entropy(bi_over) / 2
        h2_disj = entropy(bi_disj) / 2

        print(f"\n=== {name} ===")
        print(f"Довжина: {len(text)}, розмір алфавіту m = {m}, H0 = {h0:.4f}")
        print(f"Біграм: перекривних {sum(bi_over.values())}, неперекривних {sum(bi_disj.values())}")
        print(f"H1 = {h1:.4f}  (R1 = {1 - h1 / h0:.4f})")
        print(f"H2 перекривні   = {h2_over:.4f}  (R = {1 - h2_over / h0:.4f})")
        print(f"H2 неперекривні = {h2_disj:.4f}  (R = {1 - h2_disj / h0:.4f})")
        print("Топ-5 символів:", top(chars))
        print("Топ-5 біграм (перекривні):", top(bi_over))
        print("Топ-5 біграм (неперекривні):", top(bi_disj))

        save_table(OUT_DIR / f"chars_{name}.csv", chars, ["symbol", "count", "probability"])
        save_table(OUT_DIR / f"bigrams_overlap_{name}.csv", bi_over, ["bigram", "count", "probability"])
        save_table(OUT_DIR / f"bigrams_disjoint_{name}.csv", bi_disj, ["bigram", "count", "probability"])


if __name__ == "__main__":
    main()
