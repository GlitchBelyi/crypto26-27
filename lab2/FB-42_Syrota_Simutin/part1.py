INPUT_FILE = "prepared.txt"

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

KEYS = [
    "то",
    "где",
    "ежик",
    "слева",
    "тольконачинался"
]

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read()

for key in KEYS:
    encrypted = ""

    for i, char in enumerate(text):
        x = ALPHABET.index(char)
        k = ALPHABET.index(key[i % len(key)])
        y = (x + k) % len(ALPHABET)
        encrypted += ALPHABET[y]

    output_file = f"enc{len(key)}.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(encrypted)

    print(f"{output_file}")