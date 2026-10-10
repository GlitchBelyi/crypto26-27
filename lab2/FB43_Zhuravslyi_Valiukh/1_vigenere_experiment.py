from collections import Counter
from pathlib import Path

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
INDEX = {ch: i for i, ch in enumerate(ALPHABET)}

def prepare_text(text):
    text = text.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in ALPHABET)

def encrypt(text, key):
    text = prepare_text(text)
    key = prepare_text(key)

    return "".join(
        ALPHABET[(INDEX[ch] + INDEX[key[i % len(key)]]) % M]
        for i, ch in enumerate(text)
    )

def coincidence_index(text):
    text = prepare_text(text)
    n = len(text)

    if n < 2:
        return 0.0

    counts = Counter(text)

    return sum(
        count * (count - 1)
        for count in counts.values()
    ) / (n * (n - 1))

def main():
    base = Path(__file__).resolve().parent
    source_file = base / "task1_source_2_3kb.txt"

    if not source_file.exists():
        print("ПОМИЛКА: поруч зі скриптом немає task1_source_2_3kb.txt")
        return

    original_text = source_file.read_text(encoding="utf-8")
    plain = prepare_text(original_text)

    keys = [
        "да",            # r = 2
        "мир",           # r = 3
        "ключ",          # r = 4
        "тайна",         # r = 5
        "безопасность"   # r = 12
    ]

    print("ПУНКТ 1. ДОСЛІДЖЕННЯ ШИФРУ ВІЖЕНЕРА")
    print(f"Файл відкритого тексту: {source_file.name}")
    print(f"Розмір початкового файла: {len(original_text.encode('utf-8'))} байт")
    print(f"Символів після підготовки: {len(plain)}")
    print(f"IC відкритого тексту: {coincidence_index(plain):.6f}")
    print()

    print(" r | ключ         | IC шифртексту")
    print("---+--------------+--------------")

    for key in keys:
        cipher = encrypt(plain, key)
        print(
            f"{len(key):2d} | "
            f"{key:12s} | "
            f"{coincidence_index(cipher):.6f}"
        )

if __name__ == "__main__":
    main()
