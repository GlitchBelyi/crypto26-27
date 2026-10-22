import math
import re
from collections import Counter

CUSTOM_ALPHABET = "абвгдежзийклмнопрстуфхцчшщыьюя"
ALLOWED_CHARS = set(CUSTOM_ALPHABET + " ")

def clean_text(raw_data: str, keep_spaces: bool = True) -> str:
    """Функція для нормалізації тексту за вказаними правилами."""
    text = raw_data.lower()
    replacements = {"ё": "е", "ъ": "ь", "э": "е"}
    for old_char, new_char in replacements.items():
        text = text.replace(old_char, new_char)

    filtered_chars = [ch if ch in ALLOWED_CHARS else " " for ch in text]
    text = "".join(filtered_chars)
    text = re.sub(r"\s+", " ", text).strip()

    if not keep_spaces:
        text = text.replace(" ", "")    
    return text

def compute_entropy_h1(freq_dict: Counter, total_chars: int) -> float:
    """Обчислення ентропії H1 на один символ."""
    entropy = 0.0
    for count in freq_dict.values():
        probability = count / total_chars
        entropy -= probability * math.log2(probability)
    return entropy

filename = "Pyat_lojek_eliksira.txt"

try:
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        original_text = f.read()

    text_spaces = clean_text(original_text, keep_spaces=True)
    text_nospaces = clean_text(original_text, keep_spaces=False)
    variants = [
        ("Текст ІЗ пробілами", text_spaces),
        ("Текст БЕЗ пробілів", text_nospaces)
    ]

    for title, processed_text in variants:
        total_len = len(processed_text)
        char_counts = Counter(processed_text)
        h1_value = compute_entropy_h1(char_counts, total_len)

        print(f"\n=== {title} ===")
        print(f"Загальна довжина: {total_len} символів")
        print(f"Розмір алфавіту (унікальних символів): {len(char_counts)}")
        print(f"Ентропія H1: {h1_value:.5f} біт/символ")
        
        print("Топ-5 найчастіших символів:")
        for char, count in char_counts.most_common(5):
            display_char = "[пробіл]" if char == " " else char
            prob = count / total_len
            print(f"  '{display_char}': кількість = {count}, ймовірність = {prob:.5f}")

except FileNotFoundError:
    print(f"Помилка: Файл '{filename}' не знайдено.")