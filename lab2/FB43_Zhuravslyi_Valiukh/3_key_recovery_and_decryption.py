from collections import Counter
from pathlib import Path

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
INDEX = {ch: i for i, ch in enumerate(ALPHABET)}

RUS_FREQ = {
    'о':0.1097,'е':0.0849,'а':0.0801,'и':0.0735,'н':0.0670,'т':0.0626,
    'с':0.0547,'р':0.0473,'в':0.0454,'л':0.0440,'к':0.0349,'м':0.0321,
    'д':0.0298,'п':0.0281,'у':0.0262,'я':0.0201,'ы':0.0190,'ь':0.0174,
    'г':0.0170,'з':0.0165,'б':0.0159,'ч':0.0144,'й':0.0121,'х':0.0097,
    'ж':0.0094,'ш':0.0073,'ю':0.0064,'ц':0.0048,'щ':0.0036,'э':0.0032,
    'ф':0.0026,'ъ':0.0004
}
s = sum(RUS_FREQ.values())
RUS_FREQ = {k: v / s for k, v in RUS_FREQ.items()}

def prepare_text(text):
    text = text.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in ALPHABET)

def coincidence_index(text):
    n = len(text)
    counts = Counter(text)
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))

def chi_square_for_shift(column, shift):
    n = len(column)
    observed = [0] * M

    for ch in column:
        plain_index = (INDEX[ch] - shift) % M
        observed[plain_index] += 1

    score = 0.0
    for i, letter in enumerate(ALPHABET):
        expected = RUS_FREQ[letter] * n
        score += (observed[i] - expected) ** 2 / expected

    return score

def recover_key(text, r):
    key = []
    details = []

    for pos in range(r):
        column = text[pos::r]

        scores = sorted(
            (chi_square_for_shift(column, shift), shift)
            for shift in range(M)
        )

        best_score, best_shift = scores[0]
        best_char = ALPHABET[best_shift]
        key.append(best_char)

        most_char, count = Counter(column).most_common(1)[0]
        naive_shift = (INDEX[most_char] - INDEX["о"]) % M

        details.append((
            pos + 1,
            len(column),
            coincidence_index(column),
            most_char,
            ALPHABET[naive_shift],
            best_char,
            best_score
        ))

    return "".join(key), details

def decrypt(text, key):
    return "".join(
        ALPHABET[(INDEX[ch] - INDEX[key[i % len(key)]]) % M]
        for i, ch in enumerate(text)
    )

def main():
    base = Path(__file__).resolve().parent
    filename = base / "variant3_ciphertext.txt"

    if not filename.exists():
        print("ПОМИЛКА: поруч зі скриптом немає variant3_ciphertext.txt")
        return

    cipher = prepare_text(filename.read_text(encoding="utf-8"))
    r = 14

    key, details = recover_key(cipher, r)

    print("ПУНКТ 3. ВІДНОВЛЕННЯ КЛЮЧА ТА ВІДКРИТОГО ТЕКСТУ")
    print(f"Використаний період: r = {r}")
    print()
    print("pos | n   | IC       | y* | по 'о' | χ²     | символ")
    print("----+-----+----------+----+--------+--------+-------")

    for pos, n, ic, most_char, naive, best, score in details:
        print(f"{pos:3d} | {n:3d} | {ic:.6f} | {most_char}  | {naive:^6s} | {score:6.2f} | {best}")

    print(f"\nВідновлений ключ: {key}")

    plaintext = decrypt(cipher, key)
    output = base / "variant3_decrypted.txt"
    output.write_text(plaintext, encoding="utf-8")

    print(f"Розшифрований текст записано у: {output.name}")
    print("\nПочаток розшифрованого тексту:")
    print(plaintext[:1000])

if __name__ == "__main__":
    main()
