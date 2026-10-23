INPUT_FILE = "var4r.txt"
OUTPUT_FILE = "decrypted.txt"

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
KEY = "громыковедьма"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read().strip()

decrypted = ""

for i, char in enumerate(text):
    y = ALPHABET.index(char)
    k = ALPHABET.index(KEY[i % len(KEY)])
    x = (y - k) % len(ALPHABET)
    decrypted += ALPHABET[x]


print("Ключ:", KEY)
print("Довжина тексту:", len(decrypted))
print("Результат записано у:", OUTPUT_FILE)
print()
print(decrypted[:500])