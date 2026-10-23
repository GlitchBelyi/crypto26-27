from collections import Counter

INPUT_FILE = "var4r.txt"

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

KEY_LENGTH = 13

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read().strip()

key = ""

print(f"Довжина шифртексту: {len(text)}")
print()

for i in range(KEY_LENGTH):
    block = text[i::KEY_LENGTH]
    frequencies = Counter(block)

    most_common_char = frequencies.most_common(1)[0][0]

    cipher_index = ALPHABET.index(most_common_char)
    plain_index = ALPHABET.index("а")
    key_index = (cipher_index - plain_index) % len(ALPHABET)

    key_char = ALPHABET[key_index]
    key += key_char

    print(
        f"Блок {i + 1}: "
        f"{most_common_char} = {frequencies[most_common_char]} "
        f"-> ключ: {key_char}"
    )

print()
print("Попередній ключ:", key)