from collections import Counter

INPUT_FILE = "var4r.txt"

CANDIDATES = [11, 13, 14, 26, 28]

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read().strip()

for r in CANDIDATES:
    print("=" * 50)
    print(f"ДОВЖИНА КЛЮЧА: {r}")
    print("=" * 50)

    for i in range(r):
        block = text[i::r]
        frequencies = Counter(block)
        most_common = frequencies.most_common(3)

        print(
            f"Блок {i + 1:2}: "
            f"{most_common[0][0]}={most_common[0][1]}, "
            f"{most_common[1][0]}={most_common[1][1]}, "
            f"{most_common[2][0]}={most_common[2][1]}"
        )

    print()