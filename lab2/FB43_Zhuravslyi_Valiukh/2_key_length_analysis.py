from collections import Counter
from pathlib import Path

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

def prepare_text(text):
    text = text.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in ALPHABET)

def coincidence_index(text):
    n = len(text)
    if n < 2:
        return 0.0
    counts = Counter(text)
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))

def average_block_ic(text, r):
    blocks = [text[i::r] for i in range(r)]
    values = [coincidence_index(block) for block in blocks]
    return sum(values) / r

def coincidence_shift_stat(text, r):
    return sum(text[i] == text[i + r] for i in range(len(text) - r))

def main():
    base = Path(__file__).resolve().parent
    filename = base / "variant3_ciphertext.txt"

    if not filename.exists():
        print("ПОМИЛКА: поруч зі скриптом немає variant3_ciphertext.txt")
        return

    cipher = prepare_text(filename.read_text(encoding="utf-8"))

    print("ПУНКТ 2. ВИЗНАЧЕННЯ ДОВЖИНИ КЛЮЧА")
    print(f"Довжина шифртексту: {len(cipher)}")
    print()
    print(" r | середній IC | D_r")
    print("---+-------------+-----")

    results = []
    for r in range(2, 31):
        avg_ic = average_block_ic(cipher, r)
        d = coincidence_shift_stat(cipher, r)
        results.append((r, avg_ic, d))
        print(f"{r:2d} | {avg_ic:.6f}    | {d}")

    print("\nНайбільші значення середнього IC:")
    for r, avg_ic, d in sorted(results, key=lambda x: x[1], reverse=True)[:6]:
        print(f"r={r:2d}: avgIC={avg_ic:.6f}, D_r={d}")

    print("\nНайбільші значення D_r:")
    for r, avg_ic, d in sorted(results, key=lambda x: x[2], reverse=True)[:6]:
        print(f"r={r:2d}: D_r={d}, avgIC={avg_ic:.6f}")

    print("\nВисновок для варіанта 3:")
    print("Найімовірніший період ключа: r = 14.")
    print("r = 28 також дає сильний пік, оскільки 28 кратне 14.")

if __name__ == "__main__":
    main()
