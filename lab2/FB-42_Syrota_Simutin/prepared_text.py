import re

INPUT_FILE = "text.txt"

OUTPUT_FILE = "prepared.txt"

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

with open(INPUT_FILE, "r", encoding="utf-8") as file:

    text = file.read()

text = text.lower()

text = text.replace("ё", "е")

text = "".join(

    char for char in text

    if char in ALPHABET

)

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    file.write(text)