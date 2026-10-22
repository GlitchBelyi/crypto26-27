from math import gcd

ALPHABET = "абвгдежзийклмнопрстуфхцчшщыьэюя"
m = len(ALPHABET)
M = m * m

# Завдання 1
# Розширений алгоритм Евкліда
def extended_gcd(a, b):
    r0 = a
    r1 = b
    u0 = 1
    u1 = 0
    v0 = 0
    v1 = 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return r0, u0, v0

# Обернений елемент a^(-1) mod n
def mod_inverse(a, n):
    d, u, v = extended_gcd(a, n)
    if d != 1:
        return None
    return u % n


# Розв'язування ax ≡ b (mod n)
def solve_congruence(a, b, n):
    d, u, v = extended_gcd(a, n)
    # Якщо b не ділиться на d, то розв'язків нема
    if b % d != 0:
        return []
    a1 = a // d
    b1 = b // d
    n1 = n // d
    # x0 = b1 * a1^(-1) mod n1
    inverse = mod_inverse(a1, n1)
    x0 = (b1 * inverse) % n1
    solutions = []

    for i in range(d):
        x = x0 + i * n1
        solutions.append(x)
    return solutions

print("Алфавіт:", ALPHABET)
print("m =", m)
print("m^2 =", M)

print("\n          -----ЗАВДАННЯ 1-----")
print("\n1. Обернений елемент")
a = 17
n = M
inverse = mod_inverse(a, n)
print("a =", a)
print("n =", n)
print("a^(-1) =", inverse)
if inverse is not None:
    print("Перевірка:", (a * inverse) % n)
else:
    print("Оберненого елемента не існує")


print("\n2. Лінійне порівняння з одним розв'язком")
a = 5
b = 3
n = 31
solutions = solve_congruence(a, b, n)
print("5x ≡ 3 (mod 31)")
print("Розв'язки:", solutions)


print("\n3. Лінійне порівняння з декількома розв'язками")
a = 6
b = 9
n = 15
solutions = solve_congruence(a, b, n)
print("6x ≡ 9 (mod 15)")
print("Розв'язки:", solutions)

print("\n4. Лінійне порівняння без розв'язків")
a = 6
b = 8
n = 15
solutions = solve_congruence(a, b, n)
print("6x ≡ 8 (mod 15)")
print("Розв'язки:", solutions)





# Завдання 2
from pathlib import Path
from collections import Counter

def normalize_ciphertext(text):
    text = text.lower()
    result = ""
    for symbol in text:
        if symbol in ALPHABET:
            result += symbol
    return result


def calculate_bigrams(text):
    bigrams = []
    # Біграми, що не перетинаються: (y1, y2), (y3, y4)..
    for i in range(0, len(text) - 1, 2):
        bigram = text[i:i + 2]
        bigrams.append(bigram)
    counts = Counter(bigrams)
    return counts, len(bigrams)

folder = Path(__file__).resolve().parent
input_file = folder / "04.txt"
ciphertext = input_file.read_text(encoding="cp1251")
ciphertext = normalize_ciphertext(ciphertext)


print("\n\n          -----ЗАВДАННЯ 2-----\n")
print("Довжина шифртексту:", len(ciphertext))

bigram_counts, total_bigrams = calculate_bigrams(ciphertext)
print("Кількість біграм:", total_bigrams)
print("\n5 найчастіших біграм шифртексту:")
for bigram, count in bigram_counts.most_common(5):
    frequency = count / total_bigrams
    print(
        bigram,
        "- кількість:",
        count,
        "- частота:",
        round(frequency, 6)
    )
    
    
    
    
from itertools import combinations, permutations

# Завдання 3

# Перетворення біграми у число: X = x1 * m + x2
def bigram_to_number(bigram):
    x1 = ALPHABET.index(bigram[0])
    x2 = ALPHABET.index(bigram[1])
    return x1 * m + x2

language_bigrams = [
    "ст",
    "но",
    "то",
    "на",
    "ен"
]

cipher_bigrams = [
    bigram
    for bigram, count in bigram_counts.most_common(5)
]

print("\n          -----ЗАВДАННЯ 3-----")
print("\nЧасті біграми російської мови:")
print(language_bigrams)
print("\nЧасті біграми шифртексту:")
print(cipher_bigrams)


candidates = set() # Для збереження унікальних кандидатів
systems_count = 0 # Лічильник перевірених систем
no_solutions_count = 0 # Кількість систем, які не мають розв'язків
all_candidates_count = 0 # Кількість допустимих кандидатів до вилучення повторів


# Беремо дві різні біграми відкритого тексту
for plain_bigram1, plain_bigram2 in combinations(language_bigrams, 2):
    X1 = bigram_to_number(plain_bigram1)
    X2 = bigram_to_number(plain_bigram2)
    for cipher_bigram1, cipher_bigram2 in permutations(cipher_bigrams, 2):
        Y1 = bigram_to_number(cipher_bigram1)
        Y2 = bigram_to_number(cipher_bigram2)
        systems_count += 1
        A = (X1 - X2) % M
        B = (Y1 - Y2) % M
        possible_a = solve_congruence(A, B, M)
        # Якщо порівняння не має розв'язків
        if len(possible_a) == 0:
            no_solutions_count += 1
        # Для кожного можливого a знаходимо b
        for a in possible_a:
            # За означенням ключа: 0 < a < m^2
            if a == 0:
                continue
            # a повинно бути взаємно простим з m
            d, _, _ = extended_gcd(a, m)
            if d != 1:
                continue
            # b = (Y1 - aX1) mod m^2
            b = (Y1 - a * X1) % M
            all_candidates_count += 1
            candidates.add((a, b))

candidates = sorted(candidates)
print("\nКількість перевірених систем:", systems_count)
print("Систем без розв'язків:", no_solutions_count)
print("Допустимих кандидатів до вилучення повторів:", all_candidates_count)
print("Кількість унікальних кандидатів на ключ:", len(candidates))

print("\nПерші 20 кандидатів (a, b):")
for a, b in candidates[:20]:
    print("a =", a, "b =", b)

candidates_file = folder / "candidates.txt"
with candidates_file.open( "w", encoding="utf-8") as file:
    for a, b in candidates:
        file.write(f"a = {a}, b = {b}\n")

print("\nУсі кандидати збережено у файл:",  candidates_file.name)


# ---------------------------------------------------------------
# Завдання 4-5. 
# ---------------------------------------------------------------
 
def number_to_bigram(number):
    return ALPHABET[number // m] + ALPHABET[number % m]
 
 
# Дешифрування: X = a^(-1) * (Y - b) mod m^2
def decrypt_text(text, a, b):
    a_inv = mod_inverse(a, M)
    result = []
    for i in range(0, len(text) - 1, 2):
        Y = bigram_to_number(text[i:i + 2])
        X = (a_inv * (Y - b)) % M
        result.append(number_to_bigram(X))
    return "".join(result)
 
 
# Критерії змістовності російського тексту 
FREQUENT_LETTERS = "оеаинт"          # найчастіші літери (частка ≈ 0.47)
FORBIDDEN_BIGRAMS = {"ыы", "ьь", "ыь", "ьы", "йь", "йы", "ьй",
                     "яы", "юы", "ьэ", "ыэ", "эь", "эы", "йй"}
 
 
def index_of_coincidence(text):      # рос. мова ≈ 0.055, випадковий ≈ 0.032
    counts = Counter(text)
    n = len(text)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))
 
 
def frequent_letters_share(text):
    return sum(1 for ch in text if ch in FREQUENT_LETTERS) / len(text)
 
 
def forbidden_share(text):
    bad = sum(1 for i in range(len(text) - 1)
              if text[i:i + 2] in FORBIDDEN_BIGRAMS)
    return bad / (len(text) - 1)
 
 
def is_meaningful(text):
    return (frequent_letters_share(text) > 0.40
            and index_of_coincidence(text) > 0.05
            and forbidden_share(text) < 0.002)
 
 
print("\n\n          -----ЗАВДАННЯ 4-5-----")
 
# Завдання 4: дешифруємо за кожним кандидатом, сміття відкидаємо
accepted = []
for a, b in candidates:
    plain = decrypt_text(ciphertext, a, b)
    if is_meaningful(plain):
        accepted.append((frequent_letters_share(plain), a, b, plain))
accepted.sort(reverse=True)
 
print("\nПеревірено кандидатів:", len(candidates))
print("Відкинуто кандидатів:", len(candidates) - len(accepted))
print("Залишилось кандидатів:", len(accepted))
 
# Завдання 5: ключ знайдено, якщо залишився змістовний текст
if not accepted:
    print("\nЗмістовного тексту не знайдено. Спробуйте знизити пороги в is_meaningful.")
else:
    _, key_a, key_b, plaintext = accepted[0]
    print("\nЗнайдено ключ: a =", key_a, ", b =", key_b)
    print("Частка літер 'оеаинт':", round(accepted[0][0], 4))
    print("Індекс співпадінь:", round(index_of_coincidence(plaintext), 4))
 
    # Які саме пари біграм привели до цього ключа
    cipher_numbers = {bigram_to_number(c): c for c in cipher_bigrams}
    print("\nВідповідність біграм мови та шифртексту за цим ключем:")
    for lb in language_bigrams:
        Y = (key_a * bigram_to_number(lb) + key_b) % M
        if Y in cipher_numbers:
            print(f"  {lb} -> {cipher_numbers[Y]}")
 
    print("\nПочаток розшифрованого тексту:")
    print(plaintext[:500])
 
    out_file = folder / "decrypted.txt"
    out_file.write_text(plaintext, encoding="utf-8")
    print("\nПовний текст збережено у файл:", out_file.name)
 
    if len(accepted) > 1:
        print("\nІнші кандидати, що пройшли перевірку:")
        for score, a, b, _ in accepted[1:6]:
            print(f"  a = {a}, b = {b}, частка літер = {round(score, 4)}")

raw = (folder / "04.txt").read_text(encoding="cp1251").lower()
extra = Counter(ch for ch in raw if ch not in ALPHABET and not ch.isspace())
print("Символи поза алфавітом:", extra)
print("Довжина сирого тексту:", len(raw), " після нормалізації:", len(ciphertext))      
     