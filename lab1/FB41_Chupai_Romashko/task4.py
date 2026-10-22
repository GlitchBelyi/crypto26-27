import math
import random
from collections import Counter

def compute_entropy(counts: Counter, total: int) -> float:
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def compute_entropy_h1(text: str) -> float:
    counts = Counter(text)
    return compute_entropy(counts, len(text))

def get_overlapping_bigrams(text: str) -> list:
    return [text[i:i+2] for i in range(len(text) - 1)]

def get_nonoverlapping_bigrams(text: str) -> list:
    return [text[i:i+2] for i in range(0, len(text) - 1, 2)]

def calculate_h2_per_symbol(bigrams_list: list) -> float:
    counts = Counter(bigrams_list)
    total = sum(counts.values())
    h_joint = compute_entropy(counts, total)
    return h_joint / 2.0


def task4(n: int, symbols=("а", "б"), seed: int = 42):
    random.seed(seed)
    s1, s2 = symbols
    half = n // 2

    # Г — випадковий порядок 
    pool = [s1] * half + [s2] * (n - half)
    random.shuffle(pool)
    seq_G = "".join(pool)

    # Д — виражена періодична структура 
    seq_D = (s1 + s2) * (n // 2)
    if len(seq_D) < n:
        seq_D += s1

    print(f"{'Послідовність':30s} {'H1':>10s} {'H2 (перекр.)':>14s} {'H2 (неперекр.)':>16s}")
    print("-" * 74)
    for name, seq in [("Г (випадковий порядок)", seq_G), ("Д (періодична abab...)", seq_D)]:
        h1 = compute_entropy_h1(seq)
        h2_over = calculate_h2_per_symbol(get_overlapping_bigrams(seq))
        h2_nonover = calculate_h2_per_symbol(get_nonoverlapping_bigrams(seq))
        print(f"{name:30s} {h1:10.5f} {h2_over:14.5f} {h2_nonover:16.5f}")

    print(f"\nЧастоти символів Г: {dict(Counter(seq_G))}")
    print(f"Частоти символів Д: {dict(Counter(seq_D))}")


if __name__ == "__main__":
    N = 100000
    task4(N)