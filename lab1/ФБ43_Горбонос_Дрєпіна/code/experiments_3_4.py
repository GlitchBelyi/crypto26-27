import random
from collections import Counter
from pathlib import Path

from entropy_stats import entropy, ngrams

LENGTH = 200_000
SEED = 42
DATA = Path("data/text_with_spaces.txt")


def h1(seq):
    return entropy(ngrams(seq, 1, 1))


def h2(seq, step):
    return entropy(ngrams(seq, 2, step)) / 2


def report(name, seq):
    print(f"{name}: довжина={len(seq)}, символів={len(set(seq))}, "
          f"H1={h1(seq):.4f}, H2 перекр.={h2(seq, 1):.4f}, H2 неперекр.={h2(seq, 2):.4f}")


def stage3(text, rng):
    print("\n=== Розділ 3: А, Б, В ===")
    alphabet = sorted(set(text))
    seq_a = text[:LENGTH]
    seq_b = Counter(text).most_common(1)[0][0] * LENGTH
    seq_v = "".join(rng.choices(alphabet, k=LENGTH))
    print(f"Алфавіт: {len(alphabet)} символів")
    for name, seq in (("А", seq_a), ("Б", seq_b), ("В", seq_v)):
        print(f"{name}: довжина={len(seq)}, символів={len(set(seq))}, H1={h1(seq):.4f}")


def stage4(rng):
    print("\n=== Розділ 4: Г, Д ===")
    seq_d = "ab" * (LENGTH // 2)
    chars = list(seq_d)
    rng.shuffle(chars)
    seq_g = "".join(chars)
    report("Г (випадковий порядок)", seq_g)
    report("Д (abab...)", seq_d)

    letters = "абвгдежзийклмнопрстуфхцчшщыьэюя"
    seq_d32 = letters * (LENGTH // len(letters))
    chars = list(seq_d32)
    rng.shuffle(chars)
    print("\nДодатково, алфавіт з 31 літери:")
    report("Г31 (випадковий порядок)", "".join(chars))
    report("Д31 (циклічний період 31)", seq_d32)


def main():
    text = DATA.read_text(encoding="utf-8")
    rng = random.Random(SEED)
    stage3(text, rng)
    stage4(rng)


if __name__ == "__main__":
    main()
