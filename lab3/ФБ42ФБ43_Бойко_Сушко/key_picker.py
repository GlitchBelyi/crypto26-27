from collections import Counter
import math
import sys
import itertools

ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя" # Для шифротексту 01_utf8.txt (букви "ь" та "ы" обміняні місцями)
#ALPHABET = "абвгдежзийклмнопрстуфхцчшщыьэюя" # Для шифротексту V1_utf8.txt (стандартний алфавіт)

def get_encrypted_bigrams(text):
    
    bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]

    bigram_counts = Counter(bigrams)

    encr_bigrams = []

    print("=== ТОП-5 НАЙБІЛЬШ ЧАСТИХ БІГРАМ ===")

    for key in bigram_counts.most_common(5):
        print(f"'{key[0]}': {key[1]/len(bigrams):.4f}")
        encr_bigrams.append(key[0])

    return encr_bigrams

def get_bigram_order(bigrams):
    orders = []
    for bigram in bigrams:
        orders.append(ALPHABET.index(bigram[0]) * 31 + ALPHABET.index(bigram[1]))
    return orders

def get_bigram_from_order(order):
    first_letter = ALPHABET[order // 31]
    second_letter = ALPHABET[order % 31]
    return first_letter + second_letter

def get_inverted_by_module(a, m):
    try:
        inverted = pow(a, -1, m)
    except ValueError:
        inverted = None
    return inverted

def solve_modular_equation(x, y, m):
    """
    Знаходить усі значення 'a' для рівняння: x * a ≡ y (mod m)
    """

    d = math.gcd(x, m)
    
    if y % d != 0:
        return []
        
    x_prime = x // d
    y_prime = y // d
    m_prime = m // d
    
    x_inv = get_inverted_by_module(x_prime, m_prime)
    
    if x_inv is None:
        return []
    
    a0 = (y_prime * x_inv) % m_prime
    
    solutions = [(a0 + k * m_prime) for k in range(d)]
    
    return solutions

def decrypt(text, key):
    a, b = key
    decrypted_text = ""
    a_inv = get_inverted_by_module(a, 31 * 31)
    
    for i in range(0, len(text), 2):
        bigram = text[i:i+2]
        if len(bigram) < 2:
            break
        order = ALPHABET.index(bigram[0]) * 31 + ALPHABET.index(bigram[1])
        
        if a_inv is None:
            break
        decrypted_order = (a_inv * (order - b)) % (31 * 31)
        decrypted_bigram = get_bigram_from_order(decrypted_order)
        decrypted_text += decrypted_bigram

    return decrypted_text


if __name__ == "__main__":
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        raw_text = f.read()
        text = "".join(c for c in raw_text if c in ALPHABET)
    encrypted_bigrams = get_encrypted_bigrams(text)
    encrypted_orders = get_bigram_order(encrypted_bigrams)
    plain_bigrams = ['ст', 'но', 'то', 'на', 'ен']
    plain_orders = get_bigram_order(plain_bigrams)

    possible_keys = []
    m = 31 * 31

    for E_pair in itertools.combinations(encrypted_orders, 2):
        for P_pair in itertools.permutations(plain_orders, 2):
            Y1, Y2 = E_pair
            X1, X2 = P_pair

            x = (X1 - X2) % m
            y = (Y1 - Y2) % m

            solutions_a = solve_modular_equation(x, y, m)

            for a in solutions_a:
                if math.gcd(a, 31) == 1:
                    b = (Y1 - a * X1) % m
                    possible_keys.append((a, b))

    possible_keys = list(set(possible_keys))

    FORBIDDEN_BIGRAMS = {'ьь', 'ыы', 'йй', 'аь', 'оь', 'еь', 'уь', 'иь', 'ыь', 'эь', 'юь', 'яь', 'ьы', 'жы', 'шы', 'чя', 'щя'}

    text_dict = dict()

    for key in possible_keys:
        decrypted_text = decrypt(text, key)

        if not decrypted_text:
            continue

        frequencies = Counter(decrypted_text)
        total_chars = len(decrypted_text)
        h1 = 0.0
        for char in frequencies:
            p_i = frequencies[char] / total_chars
            h1 -= p_i * math.log2(p_i)

        top_chars_freq = sum(frequencies[c] / total_chars for c in 'оаеинт' if c in frequencies)


        cross_bigrams = [decrypted_text[i:i+2] for i in range(1, len(decrypted_text)-1, 2)]
        forbidden_count = sum(1 for bg in cross_bigrams if bg in FORBIDDEN_BIGRAMS)

        score = h1 - (top_chars_freq * 2) + (forbidden_count * 0.5)

        text_dict[key] = {
            'text': decrypted_text,
            'h1': h1,
            'forbidden_count': forbidden_count,
            'score': score
        }

    sorted_text_dict = dict(sorted(text_dict.items(), key=lambda item: item[1]['score']))

    print(f"\nУсього проаналізовано кандидатів на ключ: {len(sorted_text_dict)}")
    print("\n=== ТОП-10 НАЙБІЛЬШ ІМОВІРНИХ КЛЮЧІВ ТА ТЕКСТІВ ===\n")
    
    for i, (key, data) in enumerate(list(sorted_text_dict.items())[:10], 1):
        decrypted_text = data['text']
        h1 = data['h1']
        forbidden = data['forbidden_count']
        score = data['score']
        
        key_chars = f"({get_bigram_from_order(key[0])}, {get_bigram_from_order(key[1])})"
        
        print(f"[{i}] Ключ: {key} {key_chars}")
        print(f"    Ентропія H1: {h1:.4f} біт/символ | Заборонених перетинів: {forbidden} | Score: {score:.4f}")
        print(f"    Текст: {decrypted_text[:120]}...\n")