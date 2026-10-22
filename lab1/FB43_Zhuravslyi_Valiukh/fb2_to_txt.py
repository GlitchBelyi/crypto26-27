from pathlib import Path
import xml.etree.ElementTree as ET
import re

fb2_files = list(Path(__file__).parent.glob("*.fb2"))

if not fb2_files:
    raise FileNotFoundError("FB2-файл не знайдено")

fb2_path = fb2_files[0]

tree = ET.parse(fb2_path)
root = tree.getroot()

parts = []

for elem in root.iter():
    tag = elem.tag.split("}")[-1]

    if tag in {"p", "title", "subtitle", "epigraph"}:
        text = "".join(elem.itertext()).strip()

        if text:
            text = text.lower()
            text = "".join(
                char if char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                else " "
                for char in text
            )
            text = re.sub(r"\s+", " ", text).strip()

            if text:
                parts.append(text)

normalized_text = "\n\n".join(parts)

no_spaces_parts = [
    part.replace(" ", "")
    for part in parts
]

text_without_spaces = "\n\n".join(no_spaces_parts)

normalized_path = Path(__file__).parent / "russian_text_normalized.txt"
no_spaces_path = Path(__file__).parent / "russian_text_no_spaces.txt"

normalized_path.write_text(
    normalized_text,
    encoding="utf-8"
)

no_spaces_path.write_text(
    text_without_spaces,
    encoding="utf-8"
)

print("Джерело:", fb2_path)

print("Створено файл: russian_text_normalized.txt")
print(
    "Кількість символів після нормалізації:",
    len(normalized_text)
)
print(
    "Розмір:",
    normalized_path.stat().st_size,
    "байт"
)

print()

print("Створено файл: russian_text_no_spaces.txt")
print(
    "Кількість символів без пробілів:",
    len(text_without_spaces)
)
print(
    "Розмір:",
    no_spaces_path.stat().st_size,
    "байт"
)

print()

print("Правила попередньої обробки:")
print("1. Усі літери переведено у нижній регістр.")
print("2. Залишено тільки літери російського алфавіту.")
print("3. Інші символи замінено пробілами.")
print("4. Послідовності пробілів замінено одним пробілом.")
print("5. Абзаци збережено окремо.")
print("6. Для обчислень без пробілів створено окремий файл без пробілів.")

