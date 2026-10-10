from pathlib import Path

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
INDEX = {ch: i for i, ch in enumerate(ALPHABET)}

CORRECT_KEY = "экомаятникфуко"
WRONG_KEY = "юкомаятникфуко"

def prepare_text(text):
    text = text.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in ALPHABET)

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

    correct_text = decrypt(cipher, CORRECT_KEY)
    wrong_text = decrypt(cipher, WRONG_KEY)

    diff_positions = [
        i for i, (a, b) in enumerate(zip(correct_text, wrong_text))
        if a != b
    ]

    print("ПУНКТ 4. ДОСЛІДЖЕННЯ ВПЛИВУ ПОМИЛКИ У КЛЮЧІ")
    print(f"Правильний ключ: {CORRECT_KEY}")
    print(f"Помилковий ключ:  {WRONG_KEY}")
    print(f"Довжина ключа: {len(CORRECT_KEY)}")
    print(f"Кількість змінених символів: {len(diff_positions)}")
    print("Перші змінені позиції, нумерація з 1:")
    print([i + 1 for i in diff_positions[:20]])

    if len(diff_positions) > 1:
        periods = [
            diff_positions[i + 1] - diff_positions[i]
            for i in range(min(10, len(diff_positions) - 1))
        ]
        print("Відстані між першими помилками:")
        print(periods)

    print("\nПравильне розшифрування, початок:")
    print(correct_text[:700])

    print("\nРозшифрування з помилковим ключем, початок:")
    print(wrong_text[:700])

    (base / "variant3_wrong_key_decrypted.txt").write_text(
        wrong_text, encoding="utf-8"
    )

    print("\nВисновок:")
    print("Оскільки змінено один символ ключа довжини 14,")
    print("помилка повторюється періодично через кожні 14 символів.")

if __name__ == "__main__":
    main()
