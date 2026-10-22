from pathlib import Path
from collections import Counter
import math
import random


ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "


def entropy(text):
    counter = Counter(text)
    total = len(text)

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counter.values()
    )


def main():
    input_path = Path("russian_text_normalized.txt")

    if not input_path.exists():
        raise FileNotFoundError(
            "Не знайдено russian_text_normalized.txt"
        )

    text = input_path.read_text(encoding="utf-8")

    length = 100000

    A = text[:length]

    B = "а" * length

    random.seed(43)
    V = "".join(
        random.choice(ALPHABET)
        for _ in range(length)
    )

    h1_A = entropy(A)
    h1_B = entropy(B)
    h1_V = entropy(V)

    print("=" * 70)
    print("ДОСЛІДЖЕННЯ ВПЛИВУ РОЗПОДІЛУ СИМВОЛІВ НА ЕНТРОПІЮ")
    print("=" * 70)

    print()
    print("Прогноз до виконання обчислень:")
    print("Б < А < В")

    print()
    print("Результати:")

    print(f"А — природний текст:       H₁ = {h1_A:.8f} біт/символ")
    print(f"Б — один символ:           H₁ = {h1_B:.8f} біт/символ")
    print(f"В — випадковий текст:      H₁ = {h1_V:.8f} біт/символ")

    print()
    print("Порядок отриманих значень:")
    
    results = [
        ("А", h1_A),
        ("Б", h1_B),
        ("В", h1_V)
    ]

    results.sort(key=lambda x: x[1])

    print(" < ".join(item[0] for item in results))

    print()
    print("Довжина кожної послідовності:", length)
    print("Результати відповідають прогнозу:",
          results[0][0] == "Б" and
          results[1][0] == "А" and
          results[2][0] == "В")


if __name__ == "__main__":
    main()