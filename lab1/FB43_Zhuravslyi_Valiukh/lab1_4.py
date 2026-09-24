from collections import Counter
import math
import random


def entropy(counter):
    total = sum(counter.values())

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counter.values()
    )


def bigram_stats(text, step):
    counter = Counter(
        text[i:i + 2]
        for i in range(0, len(text) - 1, step)
    )

    h2 = entropy(counter) / 2

    return counter, h2


def main():
    length = 100000

    base = list(
        "а" * (length // 2) +
        "б" * (length // 2)
    )

    random.seed(43)
    random.shuffle(base)

    G = "".join(base)
    D = "аб" * (length // 2)

    h1_G = entropy(Counter(G))
    h1_D = entropy(Counter(D))

    _, h2_G_overlap = bigram_stats(G, 1)
    _, h2_G_nonoverlap = bigram_stats(G, 2)

    _, h2_D_overlap = bigram_stats(D, 1)
    _, h2_D_nonoverlap = bigram_stats(D, 2)

    print("=" * 70)
    print("ДОСЛІДЖЕННЯ ЗАЛЕЖНОСТЕЙ МІЖ СИМВОЛАМИ")
    print("=" * 70)

    print()
    print("Прогноз до виконання обчислень:")
    print("1. H₁ для Г і Д має бути однаковим або дуже близьким.")
    print("2. H₂ для Г і Д має суттєво відрізнятися.")
    print("3. Менше H₂ очікується для Д, оскільки символи мають періодичну структуру.")
    print("4. H₂ для перекривних і неперекривних біграм може відрізнятися.")

    print()
    print("Результати для Г — випадковий порядок:")
    print(f"H₁ = {h1_G:.8f} біт/символ")
    print(f"H₂ перекривні = {h2_G_overlap:.8f} біт/символ")
    print(f"H₂ неперекривні = {h2_G_nonoverlap:.8f} біт/символ")
    print(f"Різниця H₂ = {abs(h2_G_overlap - h2_G_nonoverlap):.8f}")

    print()
    print("Результати для Д — періодична структура:")
    print(f"H₁ = {h1_D:.8f} біт/символ")
    print(f"H₂ перекривні = {h2_D_overlap:.8f} біт/символ")
    print(f"H₂ неперекривні = {h2_D_nonoverlap:.8f} біт/символ")
    print(f"Різниця H₂ = {abs(h2_D_overlap - h2_D_nonoverlap):.8f}")

    print()
    print("Порівняння:")
    print(f"Різниця H₁ = {abs(h1_G - h1_D):.8f}")
    print(
        f"Різниця H₂ перекривних = "
        f"{abs(h2_G_overlap - h2_D_overlap):.8f}"
    )
    print(
        f"Різниця H₂ неперекривних = "
        f"{abs(h2_G_nonoverlap - h2_D_nonoverlap):.8f}"
    )


if __name__ == "__main__":
    main()