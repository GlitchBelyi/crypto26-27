INPUT_FILE = "var4.txt"
OUTPUT_FILE = "var4r.txt"

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read().lower()

text = "".join(char for char in text if char in ALPHABET)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(text)
