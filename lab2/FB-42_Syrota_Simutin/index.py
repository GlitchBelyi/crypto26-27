from collections import Counter

FILES = [
    "prepared.txt",
    "enc2.txt",
    "enc3.txt",
    "enc4.txt",
    "enc5.txt",
    "enc15.txt"
]

def coincidence_index(text):
    n = len(text)
    frequencies = Counter(text)

    numerator = sum(count * (count - 1) for count in frequencies.values())
    denominator = n * (n - 1)

    return numerator / denominator

for filename in FILES:
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read().strip()

    index = coincidence_index(text)

    print(f"\n{filename}:")
    print(f"Кількість символів: {len(text)}")
    print(f"Індекс відповідності: {index:.6f}")
    print()