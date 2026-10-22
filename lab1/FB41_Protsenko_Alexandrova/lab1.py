import math
import re
from collections import Counter


def clean_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read().lower()

    # Залишаємо тільки кирилицю (а-я, ё) та пробіли
    text_sp = re.sub(r"[^а-яё]", " ", raw)
    text_sp = re.sub(r"\s+", " ", text_sp).strip()
    text_nosp = text_sp.replace(" ", "")

    return text_sp, text_nosp


def calc_h1(text):
    n = len(text)
    counts = Counter(text)
    h1 = -sum((cnt / n) * math.log2(cnt / n) for cnt in counts.values())
    return h1, counts, n


def calc_h2_overlapping(text):
    bigrams = [text[i : i + 2] for i in range(len(text) - 1)]
    n = len(bigrams)
    counts = Counter(bigrams)
    h2 = -0.5 * sum((cnt / n) * math.log2(cnt / n) for cnt in counts.values())
    return h2, counts, n


def calc_h2_non_overlapping(text):
    bigrams = [text[i : i + 2] for i in range(0, len(text) - 1, 2)]
    n = len(bigrams)
    counts = Counter(bigrams)
    h2 = -0.5 * sum((cnt / n) * math.log2(cnt / n) for cnt in counts.values())
    return h2, counts, n


def print_top(counts, total, label):
    print(f"\nТОП-5 {label}:")
    for elem, cnt in counts.most_common(5):
        p = cnt / total
        print(f"  '{elem}': {cnt} разів (p = {p:.5f})")


def process_and_show(text, title):
    print(f"\n--- {title} ---")
    h1, c1, len1 = calc_h1(text)
    h2_ov, c2_ov, len2_ov = calc_h2_overlapping(text)
    h2_nov, c2_nov, len2_nov = calc_h2_non_overlapping(text)

    print(f"Загальна довжина: {len1} символів")
    print(f"H1 = {h1:.4f} біт/символ")
    print(f"H2 (що перетинаються) = {h2_ov:.4f} біт/символ")
    print(f"H2 (що НЕ перетинаються) = {h2_nov:.4f} біт/символ")

    print_top(c1, len1, "монограм (символів)")
    print_top(c2_ov, len2_ov, "біграм (що перетинаються)")
    print_top(c2_nov, len2_nov, "біграм (що НЕ перетинаються)")


if __name__ == "__main__":
    text_sp, text_nosp = clean_text("Американская трагедия.txt")

    with open("text_with_spaces.txt", "w", encoding="utf-8") as f:
        f.write(text_sp)

    with open("text_without_spaces.txt", "w", encoding="utf-8") as f:
        f.write(text_nosp)

    process_and_show(text_sp, "АНАЛІЗ ТЕКСТУ З ПРОБІЛАМИ")
    process_and_show(text_nosp, "АНАЛІЗ ТЕКСТУ БЕЗ ПРОБІЛІВ")
