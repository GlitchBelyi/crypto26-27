from collections import Counter
from itertools import permutations

# 31 літера: «ё» -> «е», «ъ» -> «ь»; порядок як у шифртекстах практикуму (ь перед ы)
ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
M = len(ALPHABET)
M2 = M * M
CORPUS_PATH = "../../lab1/ФБ-43_Коротка_Тимчак/corpus.txt"
CIPHERTEXT_PATH = "ciphertext_v4.txt"
DECRYPTED_PATH = "decrypted_v4.txt"
RESULTS_PATH = "results.txt"

# п'ять найчастіших біграм мови з методичних вказівок
LANG_TOP = ["ст", "но", "то", "на", "ен"]
FREQUENT = "оае"
RARE = "фщь"
# пороги розпізнавача: у мові частка «о,а,е» ≈ 0.27, «ф,щ,ь» ≈ 0.02;
# у випадковому тексті обидві ≈ 3/31 ≈ 0.097
FREQUENT_MIN = 0.20
RARE_MAX = 0.05


# нижній регістр, ё -> е, ъ -> ь, лишаємо тільки літери алфавіту
def normalize(text):
    text = text.lower().replace("ё", "е").replace("ъ", "ь")
    return "".join(ch for ch in text if ch in ALPHABET)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# розширений алгоритм Евкліда: повертає (d, u, v), де d = gcd(a, b) = u*a + v*b
def egcd(a, b):
    u0, u1, v0, v1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return a, u0, v0


# a^(-1) mod n, або None, якщо gcd(a, n) != 1
def inverse(a, n):
    d, u, _ = egcd(a % n, n)
    return u % n if d == 1 else None


# усі розв'язки порівняння a*x ≡ b (mod n)
def solve_linear(a, b, n):
    a, b = a % n, b % n
    d = egcd(a, n)[0]
    if b % d:
        return []
    a1, b1, n1 = a // d, b // d, n // d
    x0 = b1 * inverse(a1, n1) % n1
    return [x0 + k * n1 for k in range(d)]


# біграма (x1, x2) <-> X = x1*m + x2
def bigram_to_num(bg):
    return ALPHABET.index(bg[0]) * M + ALPHABET.index(bg[1])


def num_to_bigram(x):
    return ALPHABET[x // M] + ALPHABET[x % M]


# біграми, що не перетинаються
def bigrams(text):
    return Counter(text[i:i + 2] for i in range(0, len(text) - 1, 2))


# X = a^(-1) * (Y - b) mod m^2
def decrypt(text, a, b):
    a_inv = inverse(a, M2)
    return "".join(
        num_to_bigram(a_inv * (bigram_to_num(text[i:i + 2]) - b) % M2)
        for i in range(0, len(text) - 1, 2)
    )


# Y = (a*X + b) mod m^2
def encrypt(text, a, b):
    return "".join(
        num_to_bigram((a * bigram_to_num(text[i:i + 2]) + b) % M2)
        for i in range(0, len(text) - 1, 2)
    )


# з системи Y1 ≡ aX1 + b, Y2 ≡ aX2 + b: a(X1 - X2) ≡ Y1 - Y2, b = Y1 - aX1 (mod m^2)
def keys_from_pairs(x1, x2, y1, y2):
    X1, X2, Y1, Y2 = map(bigram_to_num, (x1, x2, y1, y2))
    keys = []
    for a in solve_linear(X1 - X2, Y1 - Y2, M2):
        # a має бути оборотним, інакше розшифрування неоднозначне
        if egcd(a, M)[0] == 1:
            keys.append((a, (Y1 - a * X1) % M2))
    return keys


# частки частих і рідкісних літер у тексті
def letter_shares(text):
    cnt = Counter(text)
    n = len(text)
    return sum(cnt[c] for c in FREQUENT) / n, sum(cnt[c] for c in RARE) / n


# розпізнавач: текст змістовний, якщо частих літер багато, а рідкісних мало
def is_meaningful(text):
    freq, rare = letter_shares(text)
    return freq >= FREQUENT_MIN and rare <= RARE_MAX


# вивід одночасно в консоль і в results.txt
out = []


def w(s=""):
    out.append(s)
    print(s)


def main():
    # перевірка відомостей про найчастіші біграми мови на корпусі з лаби 1
    corpus = normalize(read(CORPUS_PATH))
    corpus_top = bigrams(corpus).most_common(5)
    lang_freq, lang_rare = letter_shares(corpus)
    w("1. БІГРАМИ МОВИ (корпус лаби 1, біграми без перетину)")
    w(f"Топ-5 у корпусі: {', '.join(bg for bg, _ in corpus_top)}")
    w(f"Топ-5 з методички: {', '.join(LANG_TOP)}")
    w(f"Частка «{FREQUENT}» у мові = {lang_freq:.4f}, частка «{RARE}» = {lang_rare:.4f}")
    w()

    cipher = normalize(read(CIPHERTEXT_PATH))
    total = len(cipher) // 2
    cipher_top = [bg for bg, _ in bigrams(cipher).most_common(5)]
    w("2. НАЙЧАСТІШІ БІГРАМИ ШИФРТЕКСТУ (варіант 4)")
    w(f"Довжина шифртексту: {len(cipher)} літер, {total} біграм")
    w(f"{'біграма':>8}{'Y':>6}{'к-сть':>7}{'частка':>9}")
    for bg, c in bigrams(cipher).most_common(5):
        w(f"{bg:>8}{bigram_to_num(bg):>6}{c:>7}{c / total:>9.4f}")
    w()

    # 3. перебір зіставлень: (X*, X**) з мови -> (Y*, Y**) з шифртексту
    candidates = {}
    systems = no_solution = several = degenerate = 0
    for x1, x2 in permutations(LANG_TOP, 2):
        for y1, y2 in permutations(cipher_top, 2):
            systems += 1
            # gcd(X* - X**, m^2) > 1: розв'язків або немає, або їх кілька
            if egcd((bigram_to_num(x1) - bigram_to_num(x2)) % M2, M2)[0] > 1:
                degenerate += 1
            keys = keys_from_pairs(x1, x2, y1, y2)
            if not keys:
                no_solution += 1
            if len(keys) > 1:
                several += 1
            for key in keys:
                candidates.setdefault(key, (x1, x2, y1, y2))
    w("3. КАНДИДАТИ НА КЛЮЧ")
    w(f"Розглянуто систем: {systems}")
    w(f"З gcd(X* - X**, m^2) > 1: {degenerate}")
    w(f"Без допустимого розв'язку: {no_solution}, з кількома розв'язками: {several}")
    w(f"Різних кандидатів (a, b): {len(candidates)}")
    w()

    # 4. розшифрування кожним кандидатом і перевірка розпізнавачем
    w("4. РОЗПІЗНАВАННЯ ЗМІСТОВНОГО ТЕКСТУ")
    w(f"Критерій: частка «{FREQUENT}» ≥ {FREQUENT_MIN}, частка «{RARE}» ≤ {RARE_MAX}")
    results = []
    for (a, b), pairs in candidates.items():
        plain = decrypt(cipher, a, b)
        results.append((a, b, pairs, plain, *letter_shares(plain)))
    accepted = [r for r in results if is_meaningful(r[3])]
    freqs = [r[4] for r in results if r not in accepted]
    rares = [r[5] for r in results if r not in accepted]
    w(f"Відкинуті кандидати ({len(results) - len(accepted)}): "
      f"частка «{FREQUENT}» {min(freqs):.4f}–{max(freqs):.4f}, "
      f"частка «{RARE}» {min(rares):.4f}–{max(rares):.4f}")
    # кілька найкращих відкинутих — щоб показати, що до порогу вони не дотягують
    w("Найближчі до порогу відкинуті кандидати:")
    for a, b, pairs, plain, fr, rr in sorted(
        (r for r in results if r not in accepted), key=lambda r: -r[4]
    )[:3]:
        w(f"  a = {a}, b = {b}: «{FREQUENT}» {fr:.4f}, «{RARE}» {rr:.4f} -> {plain[:40]}")
    w(f"Прийняті кандидати: {len(accepted)}")
    for a, b, pairs, plain, fr, rr in accepted:
        x1, x2, y1, y2 = pairs
        w(f"  a = {a}, b = {b} ({x1}->{y1}, {x2}->{y2}): «{FREQUENT}» {fr:.4f}, «{RARE}» {rr:.4f}")
    w()

    a, b, pairs, plain, _, _ = accepted[0]
    # перевірка: повторне шифрування знайденим ключем дає вихідний шифртекст
    assert encrypt(plain, a, b) == cipher[:len(plain)]
    with open(DECRYPTED_PATH, "w", encoding="utf-8") as f:
        f.write(plain + "\n")
    w("5. РЕЗУЛЬТАТ")
    w(f"Ключ: a = {a}, b = {b}")
    w(f"a^(-1) mod {M2} = {inverse(a, M2)}")
    w(f"Найчастіші біграми ВТ: {', '.join(bg for bg, _ in bigrams(plain).most_common(5))}")
    w(f"Шифртекст:      {cipher[:100]}")
    w(f"Розшифрування:  {plain[:100]}")

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
