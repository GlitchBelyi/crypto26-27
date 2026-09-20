import collections
import math
import os
import random
import re


def find_file():
    candidates = ["text.txt", "text.txt.txt", "text"]
    for c in candidates:
        if os.path.exists(c):
            return c
    for f in os.listdir("."):
        if f.endswith(".txt"):
            return f
    raise FileNotFoundError("Не знайдено текстовий файл!")


def read_text(file_path):
    for enc in ["utf-8", "windows-1251", "cp1251"]:
        try:
            with open(file_path, "r", encoding=enc) as f:
                content = f.read()
                if len(content) > 1000:
                    return content
        except Exception:
            continue
    raise ValueError("Не вдалося прочитати файл у відомих кодуваннях")


def clean_text(raw_text):
    text = raw_text.lower()
    # Залишаємо тільки літери а-я та ё, все інше замінюємо на пробіл
    text = re.sub(r"[^а-яё]", " ", text)
    # Декілька пробілів замінюємо на один
    text = re.sub(r"\s+", " ", text).strip()
    return text, text.replace(" ", "")


def calc_h1(text):
    total = len(text)
    counts = collections.Counter(text)
    entropy = 0
    freqs = {}
    for char, cnt in counts.items():
        p = cnt / total
        freqs[char] = p
        entropy -= p * math.log2(p)
    return entropy, freqs


def calc_h2(text, step=1):
    bigrams = [text[i : i + 2] for i in range(0, len(text) - 1, step)]
    total = len(bigrams)
    counts = collections.Counter(bigrams)
    entropy = 0
    freqs = {}
    for bg, cnt in counts.items():
        p = cnt / total
        freqs[bg] = p
        entropy -= p * math.log2(p)
    return entropy / 2.0, freqs


def print_top5(freqs, name):
    print(f"\nТоп-5 ({name}):")
    sorted_items = sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:5]
    for item, p in sorted_items:
        display = f"'{item}'" if " " in item else item
        print(f"  {display:<6} -> {p:.5f}")


def main():
    filepath = find_file()
    print(f"Обробка файлу: {filepath}")
    raw = read_text(filepath)

    txt_sp, txt_nosp = clean_text(raw)
    print(f"Символів з пробілами: {len(txt_sp)}")
    print(f"Символів без пробілів: {len(txt_nosp)}")

    # 1. ТЕКСТ З ПРОБІЛАМИ
    print("\n" + "=" * 50)
    print("1. ТЕКСТ З ПРОБІЛАМИ (34 символи: 33 літери + пробіл)")
    print("=" * 50)
    h1_sp, f1_sp = calc_h1(txt_sp)
    h2_sp_cross, f2_sp_cross = calc_h2(txt_sp, step=1)
    h2_sp_nocross, f2_sp_nocross = calc_h2(txt_sp, step=2)

    h0_sp = math.log2(34)
    r_h1_sp = 1 - (h1_sp / h0_sp)
    r_h2_sp = 1 - (h2_sp_cross / h0_sp)

    print(f"H0 (максимальна ентропія): {h0_sp:.4f} біт/символ")
    print(f"H1:                        {h1_sp:.4f} біт/символ")
    print(f"H2 (з перетином, крок 1):   {h2_sp_cross:.4f} біт/символ")
    print(f"H2 (без перетину, крок 2): {h2_sp_nocross:.4f} біт/символ")
    print(f"Надлишковість за H1:       {r_h1_sp:.4f} ({r_h1_sp*100:.2f}%)")
    print(f"Надлишковість за H2:       {r_h2_sp:.4f} ({r_h2_sp*100:.2f}%)")

    print_top5(f1_sp, "символи (з пробілами)")
    print_top5(f2_sp_cross, "біграми з перетином (з пробілами)")
    print_top5(f2_sp_nocross, "біграми без перетину (з пробілами)")

    # 2. ТЕКСТ БЕЗ ПРОБІЛІВ
    print("\n" + "=" * 50)
    print("2. ТЕКСТ БЕЗ ПРОБІЛІВ (33 символи: літери а-я, ё)")
    print("=" * 50)
    h1_nosp, f1_nosp = calc_h1(txt_nosp)
    h2_nosp_cross, f2_nosp_cross = calc_h2(txt_nosp, step=1)
    h2_nosp_nocross, f2_nosp_nocross = calc_h2(txt_nosp, step=2)

    h0_nosp = math.log2(33)
    r_h1_nosp = 1 - (h1_nosp / h0_nosp)
    r_h2_nosp = 1 - (h2_nosp_cross / h0_nosp)

    print(f"H0 (максимальна ентропія): {h0_nosp:.4f} біт/символ")
    print(f"H1:                        {h1_nosp:.4f} біт/символ")
    print(f"H2 (з перетином, крок 1):   {h2_nosp_cross:.4f} біт/символ")
    print(f"H2 (без перетину, крок 2): {h2_nosp_nocross:.4f} біт/символ")
    print(f"Надлишковість за H1:       {r_h1_nosp:.4f} ({r_h1_nosp*100:.2f}%)")
    print(f"Надлишковість за H2:       {r_h2_nosp:.4f} ({r_h2_nosp*100:.2f}%)")

    print_top5(f1_nosp, "символи (без пробілів)")
    print_top5(f2_nosp_cross, "біграми з перетином (без пробілів)")
    print_top5(f2_nosp_nocross, "біграми без перетину (без пробілів)")

    # 3. ДОСЛІДЖЕННЯ РОЗПОДІЛІВ (РОЗДІЛ 3)
    print("\n" + "=" * 50)
    print("РОЗДІЛ 3. ВПЛИВ РОЗПОДІЛУ СИМВОЛІВ")
    print("=" * 50)
    n = 100000
    alpha = list(set(txt_nosp))
    seq_a = txt_nosp[:n]
    seq_b = "а" * n
    seq_v = "".join(random.choices(alpha, k=n))

    h1_a, _ = calc_h1(seq_a)
    h1_b, _ = calc_h1(seq_b)
    h1_v, _ = calc_h1(seq_v)

    print(f"Послідовність А (природний текст):       H1 = {h1_a:.4f}")
    print(f"Послідовність Б (один символ 'а'):        H1 = {h1_b:.4f}")
    print(f"Послідовність В (рівноймовірна випадкова): H1 = {h1_v:.4f}")

    # 4. ДОСЛІДЖЕННЯ ЗАЛЕЖНОСТЕЙ (РОЗДІЛ 4)
    print("\n" + "=" * 50)
    print("РОЗДІЛ 4. ЗАЛЕЖНОСТІ МІЖ СИМВОЛАМИ")
    print("=" * 50)
    half = n // 2
    lst_g = ["а"] * half + ["б"] * half
    random.shuffle(lst_g)
    seq_g = "".join(lst_g)
    seq_d = "аб" * half

    h1_g, _ = calc_h1(seq_g)
    h2_g_c, _ = calc_h2(seq_g, step=1)
    h2_g_nc, _ = calc_h2(seq_g, step=2)

    h1_d, _ = calc_h1(seq_d)
    h2_d_c, _ = calc_h2(seq_d, step=1)
    h2_d_nc, _ = calc_h2(seq_d, step=2)

    print(
        f"Послідовність Г (випадковий порядок 'а' та 'б'):\n  H1 = {h1_g:.4f}, H2(перетин) = {h2_g_c:.4f}, H2(без перетину) = {h2_g_nc:.4f}"
    )
    print(
        f"Послідовність Д (періодична 'абаб...'):\n  H1 = {h1_d:.4f}, H2(перетин) = {h2_d_c:.4f}, H2(без перетину) = {h2_d_nc:.4f}"
    )


if __name__ == "__main__":
    main()