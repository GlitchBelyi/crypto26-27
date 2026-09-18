import math
import random
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).parent
TEXT_FILE = BASE / "text.txt"
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
SEQ_LEN = 100000
SEED = 42
COOLPINK = {10: None, 20: None, 30: None}


def load_text(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().lower().replace("ё", "е")
    return re.sub(f"[^{ALPHABET}]+", " ", text).strip()


def entropy(counter):
    total = sum(counter.values())
    return abs(sum(c / total * math.log2(c / total) for c in counter.values()))


def ngrams(text, n, step):
    return Counter(text[i:i + n] for i in range(0, len(text) - n + 1, step))


def h1(text):
    return entropy(Counter(text))


def h2(text, step):
    return entropy(ngrams(text, 2, step)) / 2


def redundancy(h, m):
    return 1 - h / math.log2(m)


def show(item):
    return item.replace(" ", "_")


def print_top(counter, k=5):
    total = sum(counter.values())
    for item, c in counter.most_common(k):
        print(f"  {show(item):<4} {c:>9}  {c / total:.6f}")


def analyze(text, tag, m):
    chars = Counter(text)
    bi_over = ngrams(text, 2, 1)
    bi_non = ngrams(text, 2, 2)
    res = {
        "H1": entropy(chars),
        "H2 (перетин)": entropy(bi_over) / 2,
        "H2 (без перетину)": entropy(bi_non) / 2,
    }

    print(f"ТЕКСТ {tag.upper()}")
    print(f"Символів: {len(text)}, різних: {len(chars)}, m = {m}, H0 = {math.log2(m):.6f}")
    for name, value in res.items():
        print(f"{name} = {value:.6f}  R = {redundancy(value, m):.6f}")

    if res["H1"] > math.log2(m) or res["H2 (перетин)"] > res["H1"] + 1e-3:
        print("УВАГА: H1 > H0 або H2 > H1, перевірте обробку тексту")

    print("\nТоп-5 символів:")
    print_top(chars)
    print("\nТоп-5 біграм (перетин):")
    print_top(bi_over)
    print("\nТоп-5 біграм (без перетину):")
    print_top(bi_non)

    return res


def section3(text_no_spaces):
    n = min(SEQ_LEN, len(text_no_spaces))
    sequences = {
        "А (природний текст)": text_no_spaces[:n],
        "Б (один символ)": "а" * n,
        "В (рівноймовірна)": "".join(random.choices(ALPHABET, k=n)),
    }
    print("3. ВПЛИВ РОЗПОДІЛУ СИМВОЛІВ")
    print(f"Довжина: {n}, log2({len(ALPHABET)}) = {math.log2(len(ALPHABET)):.6f}")
    for name, seq in sequences.items():
        print(f"{name}: H1 = {h1(seq):.6f}, H2 (перетин) = {h2(seq, 1):.6f}")


def section4():
    periodic = "ab" * (SEQ_LEN // 2)
    chars = list(periodic)
    random.shuffle(chars)
    sequences = {"Г (випадкова)": "".join(chars), "Д (періодична)": periodic}
    print("4. ЗАЛЕЖНОСТІ МІЖ СИМВОЛАМИ")
    for name, seq in sequences.items():
        print(f"\n{name}: частоти символів {dict(Counter(seq))}")
        print(f"  біграми (перетин): {dict(ngrams(seq, 2, 1))}")
        print(f"  біграми (без перетину): {dict(ngrams(seq, 2, 2))}")
        print(f"  H1 = {h1(seq):.6f}")
        print(f"  H2 (перетин) = {h2(seq, 1):.6f}")
        print(f"  H2 (без перетину) = {h2(seq, 2):.6f}")


def section6(res_spaces, res_no_spaces):
    print("6. НАДЛИШКОВІСТЬ R = 1 - H / H0")
    cases = (
        ("з пробілами", res_spaces, len(ALPHABET) + 1),
        ("без пробілів", res_no_spaces, len(ALPHABET)),
    )
    for tag, res, m in cases:
        estimates = dict(res)
        estimates.update({f"H({n})": v for n, v in COOLPINK.items() if v is not None})
        print(f"\nТекст {tag} (m = {m}, H0 = {math.log2(m):.6f}):")
        for name, h in estimates.items():
            print(f"  {name:<18} = {h:.4f}   R = {redundancy(h, m):.4f}")


def main():
    random.seed(SEED)
    text = load_text(TEXT_FILE)
    text_no_spaces = text.replace(" ", "")
    print(f"Після обробки: {len(text)} символів, без пробілів: {len(text_no_spaces)}")

    res_spaces = analyze(text, "з пробілами", len(ALPHABET) + 1)
    res_no_spaces = analyze(text_no_spaces, "без пробілів", len(ALPHABET))
    section3(text_no_spaces)
    section4()
    section6(res_spaces, res_no_spaces)

if __name__ == "__main__":
    main()