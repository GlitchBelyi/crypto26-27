"""
Комп'ютерний практикум №1 з криптографії.
Експериментальна оцінка ентропії на символ джерела відкритого тексту.

Скрипт нічого не вигадує: усі числа, що він виводить, обчислені
безпосередньо з тексту, який ви йому передасте. Якщо файлу з текстом
немає — скрипт не запуститься, а не підставить випадкові цифри.

ПРИПУЩЕННЯ ЩОДО АЛФАВІТУ (методичка явно не задає список символів):
Алфавіт Z = {а..я, ё, пробіл} — 33 літери російського алфавіту (без "ъ"
не виключаємо, він у алфавіті лишається) + символ "ё" прирівнюємо до "е"
(це стандартна практика для таких лабораторних, тому що "ё" зустрічається
рідко і роздільна лексикографія з нею ускладнює підрахунок без користі
для суті роботи) + пробіл. Розділові знаки, цифри, латиниця, переноси
рядків і т.д. вважаються "не належними алфавіту" і замінюються пробілом.
Якщо ваш викладач вимагає інший алфавіт (наприклад, окрему "ё" або "ъ"/"ь"
виключно як м'який/твердий знак без об'єднання) — заміните ALPHABET нижче
і перезапустіть скрипт; усі розрахунки далі не залежать від конкретного
списку символів.

Запуск:
    python entropy_lab.py --input my_text.txt --outdir results main.py"""

import argparse
import json
import math
import random
import re
import unicodedata
from collections import Counter
from pathlib import Path


# 1. АЛФАВІТ І PREPROCESSING


RUSSIAN_LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"  # без ё (зводимо ё->е)
ALPHABET_WITH_SPACE = set(RUSSIAN_LETTERS + " ")


def preprocess(raw_text: str, keep_spaces: bool = True) -> str:
    """Детермінований preprocessing тексту згідно з правилами методички:
    1) нижній регістр;
    2) ё -> е (наше явне припущення, зазначене вище);
    3) символи поза алфавітом -> пробіл;
    4) послідовності пробілів/розділових знаків -> один пробіл;
    5) (опційно) повне вилучення пробілів для "варіанту без пробілів".
    """
    text = raw_text.lower()
    text = unicodedata.normalize("NFC", text)
    text = text.replace("ё", "е")

    # усе, що не входить в алфавіт (літери + пробіл) -> пробіл
    text = "".join(ch if ch in ALPHABET_WITH_SPACE else " " for ch in text)

    # послідовності пробілів -> один пробіл
    text = re.sub(r" +", " ", text).strip()

    if not keep_spaces:
        text = text.replace(" ", "")

    return text



# 2. СТАТИСТИКА СИМВОЛІВ І БІГРАМ


def char_frequencies(text: str) -> Counter:
    return Counter(text)


def entropy_from_counts(counts: Counter, total: int) -> float:
    """H = -sum p_i log2 p_i за заданими частотами."""
    h = 0.0
    for c in counts.values():
        p = c / total
        if p > 0:
            h -= p * math.log2(p)
    return h


def bigrams_overlapping(text: str):
    """(x1x2),(x2x3),(x3x4),... -- зміщення на 1 символ."""
    return [text[i:i + 2] for i in range(len(text) - 1)]


def bigrams_nonoverlapping(text: str):
    """(x1x2),(x3x4),... -- зміщення на 2 символи (немає перетину)."""
    return [text[i:i + 2] for i in range(0, len(text) - 1, 2)]


def h2_per_symbol(bigram_list) -> float:
    """H2 = H(біграми)/2. Ділимо на 2, бо ентропія рахується для об'єкта
    з двох символів, а нас цікавить ентропія В РОЗРАХУНКУ НА ОДИН СИМВОЛ
    (щоб мати змогу порівнювати з H1)."""
    counts = Counter(bigram_list)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    h_joint = entropy_from_counts(counts, total)
    return h_joint / 2.0


def top_n(counts: Counter, n: int = 5):
    return counts.most_common(n)


def analyze_text(text: str, label: str) -> dict:
    """Повний блок статистики (H1, H2 перекр./неперекр., топ-5) для тексту."""
    total_chars = len(text)
    char_counts = char_frequencies(text)
    h1 = entropy_from_counts(char_counts, total_chars)

    bg_over = bigrams_overlapping(text)
    bg_nonover = bigrams_nonoverlapping(text)

    h2_over = h2_per_symbol(bg_over)
    h2_nonover = h2_per_symbol(bg_nonover)

    return {
        "label": label,
        "total_chars": total_chars,
        "alphabet_size": len(char_counts),
        "H1": h1,
        "H2_overlapping": h2_over,
        "H2_nonoverlapping": h2_nonover,
        "top5_chars": [(ch if ch != " " else "␣", n) for ch, n in top_n(char_counts, 5)],
        "top5_bigrams_overlapping": [(bg.replace(" ", "␣"), n) for bg, n in top_n(Counter(bg_over), 5)],
        "top5_bigrams_nonoverlapping": [(bg.replace(" ", "␣"), n) for bg, n in top_n(Counter(bg_nonover), 5)],
        "n_bigrams_overlapping": len(bg_over),
        "n_bigrams_nonoverlapping": len(bg_nonover),
    }



# 3. ЕКСПЕРИМЕНТ А / Б / В (вплив розподілу символів на H1)

def experiment_abv(natural_text: str, length: int, seed: int = 42) -> dict:
    rng = random.Random(seed)

    # А - фрагмент природного тексту (беремо перші `length` символів
    # ВЖЕ ПІСЛЯ preprocessing без пробілів, щоб алфавіт збігався з В)
    seq_a = natural_text[:length]

    # Б - повторення одного символу (обираємо найчастіший символ природного
    # тексту, щоб послідовність була змістовно пов'язана з тим самим джерелом)
    most_common_char = Counter(natural_text).most_common(1)[0][0]
    seq_b = most_common_char * length

    # В - випадкова рівноймовірна послідовність з того самого алфавіту
    alphabet = sorted(set(natural_text))
    seq_v = "".join(rng.choice(alphabet) for _ in range(length))

    results = {}
    for name, seq in [("A", seq_a), ("B", seq_b), ("V", seq_v)]:
        counts = Counter(seq)
        results[name] = {
            "length": len(seq),
            "H1": entropy_from_counts(counts, len(seq)),
            "alphabet_used": len(counts),
        }
    results["seed"] = seed
    return results



# 4. ЕКСПЕРИМЕНТ Г / Д (вплив порядку символів на H2 при однакових H1)

def experiment_gd(natural_text: str, length: int, seed: int = 42) -> dict:
    rng = random.Random(seed)

    base = natural_text[:length]
    # Г - ті самі символи (той самий мультимножина частот!), випадково
    # перемішані -> частоти окремих символів ідентичні базовому фрагменту.
    chars_g = list(base)
    rng.shuffle(chars_g)
    seq_g = "".join(chars_g)

    # Д - періодична структура abababab... з таким самим алфавітом і
    # максимально близькими частотами. Будуємо як циклічне повторення
    # відсортованого алфавіту (кожен символ повторюється пропорційно
    # своїй частоті у base, порядок циклічний -> яскраво виражена
    # передбачувана структура).
    counts = Counter(base)
    symbols_sorted = sorted(counts.keys())
    # будуємо послідовність-патерн, що містить кожен символ рівно
    # стільки разів, скільки треба, циклічно чергуючи символи алфавіту
    pattern_pool = []
    remaining = dict(counts)
    while sum(remaining.values()) > 0:
        for s in symbols_sorted:
            if remaining.get(s, 0) > 0:
                pattern_pool.append(s)
                remaining[s] -= 1
    seq_d = "".join(pattern_pool)

    out = {}
    for name, seq in [("G", seq_g), ("D", seq_d)]:
        c = Counter(seq)
        out[name] = {
            "length": len(seq),
            "H1": entropy_from_counts(c, len(seq)),
            "H2_overlapping": h2_per_symbol(bigrams_overlapping(seq)),
            "H2_nonoverlapping": h2_per_symbol(bigrams_nonoverlapping(seq)),
        }
    out["seed"] = seed
    return out



# 5. НАДЛИШКОВІСТЬ

def redundancy(h_estimate: float, alphabet_size: int) -> float:
    """R = 1 - H/H0, де H0 = log2(m) -- максимально можлива ентропія
    для рівноімовірного алфавіту з m символів."""
    h0 = math.log2(alphabet_size)
    return 1 - h_estimate / h0


# MAIN

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="шлях до текстового файлу (>=1MB)")
    ap.add_argument("--outdir", default="results", help="куди зберегти results.json")
    ap.add_argument("--exp-length", type=int, default=20000,
                     help="довжина послідовностей для експериментів А/Б/В і Г/Д")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    raw = Path(args.input).read_text(encoding="utf-8", errors="ignore")
    if len(raw.encode("utf-8")) < 1_000_000:
        print(f"УВАГА: файл {args.input} має розмір "
              f"{len(raw.encode('utf-8'))} байт (<1 МБ). Методичка вимагає >=1MB. "
              f"Скрипт продовжить роботу, але для звіту потрібен більший текст.")

    text_with_spaces = preprocess(raw, keep_spaces=True)
    text_no_spaces = preprocess(raw, keep_spaces=False)

    report = {}
    report["with_spaces"] = analyze_text(text_with_spaces, "з пробілами")
    report["no_spaces"] = analyze_text(text_no_spaces, "без пробілів")

    report["experiment_ABV"] = experiment_abv(text_no_spaces, args.exp_length, seed=args.seed)
    report["experiment_GD"] = experiment_gd(text_no_spaces, args.exp_length, seed=args.seed)

    # надлишковість для наближень H1 і H2 (перекривні), окремо для варіанту
    # з пробілами і без -- бо розмір алфавіту m різний в цих двох випадках
    for key in ("with_spaces", "no_spaces"):
        m = report[key]["alphabet_size"]
        report[key]["redundancy_H1"] = redundancy(report[key]["H1"], m)
        report[key]["redundancy_H2_overlapping"] = redundancy(report[key]["H2_overlapping"], m)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / "results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # людяний друк у консоль
    for key in ("with_spaces", "no_spaces"):
        r = report[key]
        print(f"\n=== {r['label'].upper()} ===")
        print(f"Довжина тексту: {r['total_chars']} символів, розмір алфавіту: {r['alphabet_size']}")
        print(f"H1  = {r['H1']:.4f} біт/символ")
        print(f"H2 (перекривні)    = {r['H2_overlapping']:.4f} біт/символ")
        print(f"H2 (неперекривні)  = {r['H2_nonoverlapping']:.4f} біт/символ")
        print(f"Топ-5 символів: {r['top5_chars']}")
        print(f"Топ-5 біграм (перекр.): {r['top5_bigrams_overlapping']}")
        print(f"Надлишковість (за H1): {r['redundancy_H1']:.4f}")
        print(f"Надлишковість (за H2, перекр.): {r['redundancy_H2_overlapping']:.4f}")

    print("\n=== ЕКСПЕРИМЕНТ А/Б/В ===")
    print(json.dumps(report["experiment_ABV"], ensure_ascii=False, indent=2))

    print("\n=== ЕКСПЕРИМЕНТ Г/Д ===")
    print(json.dumps(report["experiment_GD"], ensure_ascii=False, indent=2))

    print(f"\nПовний результат збережено в {outdir / 'results.json'}")


if __name__ == "__main__":
    main()