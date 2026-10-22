import math
import re
from collections import Counter

CUSTOM_ALPHABET = "абвгдежзийклмнопрстуфхцчшщыьюя"
ALLOWED_CHARS = set(CUSTOM_ALPHABET + " ")

def clean_text(raw_data: str, keep_spaces: bool = True) -> str:
    """Нормалізація тексту за встановленими правилами."""
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

def compute_entropy(counts: Counter, total: int) -> float:
    """Загальна функція для обчислення ентропії."""
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy

def get_overlapping_bigrams(text: str) -> list:
    """Генерація біграм, що перетинаються (зміщення на 1)."""
    return [text[i:i+2] for i in range(len(text) - 1)]

def get_nonoverlapping_bigrams(text: str) -> list:
    """Генерація біграм, що не перетинаються (зміщення на 2)."""
    return [text[i:i+2] for i in range(0, len(text) - 1, 2)]

def calculate_h2_per_symbol(bigrams_list: list) -> float:
    """Обчислення H2 на символ джерела."""
    counts = Counter(bigrams_list)
    total_bigrams = sum(counts.values())
    h_joint = compute_entropy(counts, total_bigrams)
    return h_joint / 2.0

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
        bg_overlap = get_overlapping_bigrams(processed_text)
        bg_nonoverlap = get_nonoverlapping_bigrams(processed_text)
        h2_overlap = calculate_h2_per_symbol(bg_overlap)
        h2_nonoverlap = calculate_h2_per_symbol(bg_nonoverlap)
        print(f"\n=== {title} ===")
        print(f"Кількість перекривних біграм:   {len(bg_overlap)}")
        print(f"Кількість неперекривних біграм: {len(bg_nonoverlap)}")
        print(f"H2 (перекривні):   {h2_overlap:.5f} біт/символ")
        print(f"H2 (неперекривні): {h2_nonoverlap:.5f} біт/символ")
        print("Топ-5 біграм (перекривні):")
        top_5_overlap = Counter(bg_overlap).most_common(5)
        for bg, count in top_5_overlap:
            display_bg = bg.replace(" ", "[_]")
            print(f"  '{display_bg}': {count}")
            

except FileNotFoundError:
    print(f"Помилка: Файл '{filename}' не знайдено.")