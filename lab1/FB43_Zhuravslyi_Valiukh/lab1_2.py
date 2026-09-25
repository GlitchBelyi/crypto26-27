from pathlib import Path
from collections import Counter
import math
import csv


def entropy(counter):
    total = sum(counter.values())

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counter.values()
    )


def get_bigrams(text, step):
    return Counter(
        text[i:i + 2]
        for i in range(0, len(text) - 1, step)
    )


def print_top(counter, title):
    print(title)

    for item, count in counter.most_common(5):
        probability = count / sum(counter.values())

        if item == " ":
            item = "[пробіл]"

        print(
            f"  {item!r:12s} "
            f"частота = {count:8d} "
            f"ймовірність = {probability:.8f}"
        )


def analyze_text(text, name):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    characters = Counter(text)

    h1 = entropy(characters)

    bigrams_overlap = get_bigrams(text, 1)
    bigrams_nonoverlap = get_bigrams(text, 2)

    h2_overlap = entropy(bigrams_overlap) / 2
    h2_nonoverlap = entropy(bigrams_nonoverlap) / 2

    print(f"Кількість символів: {len(text)}")
    print(f"Кількість пересічних біграм: {len(text) - 1}")
    print(f"Кількість непересічних біграм: {len(text) // 2}")

    print()
    print(f"H₁ = {h1:.8f} біт/символ")
    print(f"H₂ для пересічних біграм = {h2_overlap:.8f} біт/символ")
    print(f"H₂ для непересічних біграм = {h2_nonoverlap:.8f} біт/символ")
    print(f"Різниця між H₂ = {abs(h2_overlap - h2_nonoverlap):.8f}")

    print()

    print_top(
        characters,
        "5 символів з найбільшою частотою:"
    )

    print()

    print_top(
        bigrams_overlap,
        "5 найбільш частих пересічних біграм:"
    )

    print()

    print_top(
        bigrams_nonoverlap,
        "5 найбільш частих непересічних біграм:"
    )

    return [
        name,
        len(text),
        h1,
        h2_overlap,
        h2_nonoverlap,
        abs(h2_overlap - h2_nonoverlap),
        len(text) - 1,
        len(text) // 2
    ]


def save_frequencies(path, counter):
    total = sum(counter.values())

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "Елемент",
            "Частота",
            "Ймовірність"
        ])

        for item, count in counter.most_common():
            if item == " ":
                item = "[пробіл]"

            writer.writerow([
                item,
                count,
                count / total
            ])


def main():
    normalized_path = Path("russian_text_normalized.txt")
    no_spaces_path = Path("russian_text_no_spaces.txt")

    if not normalized_path.exists():
        raise FileNotFoundError(
            "Не знайдено russian_text_normalized.txt"
        )

    if not no_spaces_path.exists():
        raise FileNotFoundError(
            "Не знайдено russian_text_no_spaces.txt"
        )

    text_with_spaces = normalized_path.read_text(
        encoding="utf-8"
    )

    text_without_spaces = no_spaces_path.read_text(
        encoding="utf-8"
    )

    results = []

    results.append(
        analyze_text(
            text_with_spaces,
            "НОРМАЛІЗОВАНИЙ ТЕКСТ З ПРОБІЛАМИ"
        )
    )

    results.append(
        analyze_text(
            text_without_spaces,
            "НОРМАЛІЗОВАНИЙ ТЕКСТ БЕЗ ПРОБІЛІВ"
        )
    )

    with Path("entropy_summary.csv").open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "Текст",
            "Кількість символів",
            "H1",
            "H2 пересічні",
            "H2 непересічні",
            "Різниця H2",
            "Кількість пересічних біграм",
            "Кількість непересічних біграм"
        ])

        writer.writerows(results)


    print("\nРезультати збережено у файл: entropy_summary.csv")


if __name__ == "__main__":
    main()
