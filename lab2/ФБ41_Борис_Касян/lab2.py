from pathlib import Path
from collections import Counter

#ЗАВДАННЯ 1

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

def normalize_text(text):
    text = text.lower()
    text = text.replace("ё", "е")
    result = ""
    for symbol in text:
        if symbol in ALPHABET:
            result += symbol
    return result

folder = Path(__file__).resolve().parent
input_file = folder / "open_text.txt"
text = input_file.read_text(encoding="utf-8")
normalized_text = normalize_text(text)
file_size_kb = input_file.stat().st_size / 1024

print("Початкова кількість символів:", len(text))
print("Після нормалізації:", len(normalized_text))
print("Розмір початкового файлу:", round(file_size_kb, 2), "КБ")
print("Перші 200 символів нормалізованого тексту:")
print(normalized_text[:200])

def vigenere_encrypt(text, key):
    result = ""
    for i in range(len(text)):
        x = ALPHABET.index(text[i])
        k = ALPHABET.index(key[i % len(key)])
        y = (x + k) % len(ALPHABET)
        result += ALPHABET[y]
    return result


def vigenere_decrypt(text, key):
    result = ""
    for i in range(len(text)):
        y = ALPHABET.index(text[i])
        k = ALPHABET.index(key[i % len(key)])
        x = (y - k) % len(ALPHABET)
        result += ALPHABET[x]
    return result

keys = [
    "да",            # довжина 2
    "мир",           # довжина 3
    "луна",          # довжина 4
    "книга",         # довжина 5
    "криптография"   # довжина 12
]
    
ciphertexts = {} 

print("\n----- Шифрування Віженера -----")
for key in keys:
    cipher_text = vigenere_encrypt(normalized_text, key)

    ciphertexts[key] = cipher_text

    print("\nКлюч:", key)
    print("Довжина ключа:", len(key))
    print("Перші 100 символів шифртексту:")
    print(cipher_text[:100])  
     
def coincidence_index(text):
    counts = Counter(text)
    n = len(text)
    numerator = 0
    for count in counts.values():
        numerator += count * (count - 1)
    return numerator / (n * (n - 1))

print("\n----- Індекси відповідності -----")
open_ic = coincidence_index(normalized_text)

print("Відкритий текст:", round(open_ic, 6))
for key in keys:
    ic = coincidence_index(ciphertexts[key])
    print(
        "Ключ:", key,
        "| довжина:", len(key),
        "| I =", round(ic, 6)
    )
    

#ЗАВДАННЯ 2

print("\n----- Криптоаналіз варіанта 4 -----")
variant_file = folder / "variant4.txt"
variant_text_raw = variant_file.read_text(encoding="utf-8")
variant_text = normalize_text(variant_text_raw)

print("Кількість символів у файлі:", len(variant_text_raw))
print("Кількість символів після очищення:", len(variant_text))
print("Перші 100 символів:")
print(variant_text[:100])
print("Останні 100 символів:")
print(variant_text[-100:])



def average_ic_for_period(text, r):
    blocks = []
    for i in range(r):
        block = text[i::r]
        blocks.append(block)
    indices = []
    for block in blocks:
        ic = coincidence_index(block)
        indices.append(ic)
    average_ic = sum(indices) / len(indices)
    return average_ic

print("\n----- Пошук довжини ключа за індексом відповідності -----")
ic_results = {}
for r in range(2, 31):
    avg_ic = average_ic_for_period(variant_text, r)
    ic_results[r] = avg_ic
    print(
        "r =", r,
        "| середній I =", round(avg_ic, 6)
    )




def coincidence_statistic(text, r):
    d = 0
    for i in range(len(text) - r):
        if text[i] == text[i + r]:
            d += 1
    return d

print("\n----- Статистика збігів D_r -----")
d_results = {}
for r in range(6, 31):
    d = coincidence_statistic(variant_text, r)
    d_results[r] = d
    print("r =", r, "| D_r =", d)




print("\n----- Аналіз блоків для r = 13 -----")
r = 13
for i in range(r):
    block = variant_text[i::r]
    counts = Counter(block)
    most_common = counts.most_common(5)
    print("\nБлок", i)
    print("Довжина:", len(block))
    print("Топ-5 символів:", most_common)




print("\n----- Початкове відновлення ключа -----")
r = 13
most_probable_plain = "о"
key = ""
for i in range(r):
    block = variant_text[i::r]
    counts = Counter(block)
    most_common_cipher = counts.most_common(1)[0][0]
    y = ALPHABET.index(most_common_cipher)
    x = ALPHABET.index(most_probable_plain)
    k = (y - x) % len(ALPHABET)
    key += ALPHABET[k]
    print(
        "Блок", i,
        "| найчастіша:", most_common_cipher,
        "| символ ключа:", ALPHABET[k]
    )
print("\nПочатковий ключ:", key)




print("\n----- Частоти російської мови з ЛР1 -----")
reference_file = folder / "text_lab1.txt"
reference_raw = reference_file.read_text(encoding="utf-8")
reference_text = normalize_text(reference_raw)
reference_counts = Counter(reference_text)
reference_total = len(reference_text)
reference_freq = {}


for letter in ALPHABET:
    reference_freq[letter] = reference_counts[letter] / reference_total

top_reference = sorted(
    reference_freq.items(),
    key=lambda x: x[1],
    reverse=True
)

print("Кількість символів:", reference_total)
print("Топ-10 символів:")
for letter, p in top_reference[:10]:
    print(letter, round(p, 6))
    
language_ic = sum(p ** 2 for p in reference_freq.values())
print(
    "Теоретичний індекс відповідності за частотами ЛР1:",
    round(language_ic, 6)
)








print("\n----- Уточнення ключа за методикою -----")

r = 13

# Найчастіші літери з ЛР1
most_probable_letters = [
    letter for letter, p in top_reference[:5]
]

print("Найчастіші літери з ЛР1:", most_probable_letters)

print("\nКандидати для кожного блока:")

for i in range(r):
    block = variant_text[i::r]

    y_star = Counter(block).most_common(1)[0][0]
    y = ALPHABET.index(y_star)

    candidates = []

    for x_star in most_probable_letters:
        x = ALPHABET.index(x_star)

        k = (y - x) % len(ALPHABET)
        key_letter = ALPHABET[k]

        candidates.append((x_star, key_letter))

    print(
        "Блок", i,
        "| y* =", y_star,
        "| кандидати:", candidates
    )


chosen_plain_letters = [
    "о",  # блок 0
    "о",  # блок 1
    "о",  # блок 2
    "о",  # блок 3
    "а",  # блок 4
    "о",  # блок 5
    "а",  # блок 6
    "о",  # блок 7
    "е",  # блок 8
    "о",  # блок 9
    "е",  # блок 10
    "о",  # блок 11
    "о"   # блок 12
]

refined_key = ""

print("\n----- Відновлення ключа -----")

for i in range(r):
    block = variant_text[i::r]

    y_star = Counter(block).most_common(1)[0][0]
    x_star = chosen_plain_letters[i]

    y = ALPHABET.index(y_star)
    x = ALPHABET.index(x_star)

    k = (y - x) % len(ALPHABET)
    key_letter = ALPHABET[k]

    refined_key += key_letter

    print(
        "Блок", i,
        "| y* =", y_star,
        "| x* =", x_star,
        "| k =", key_letter
    )

print("\nУточнений ключ:", refined_key)

decrypted_text = vigenere_decrypt(variant_text, refined_key)
print("\n----- Перевірка розшифрування -----")
print("Ключ:", refined_key)
print("\nПерші 500 символів:")
print(decrypted_text[:500])



# ЗАВДАННЯ 4

print("\n----- Експеримент зі зміненим ключем -----")
# Змінюємо один символ правильного ключа
wrong_key = "дромыковедьма"
print("Правильний ключ:", refined_key)
print("Ключ з помилкою:", wrong_key)

# Повторне розшифрування
wrong_decrypted_text = vigenere_decrypt(variant_text, wrong_key)
# Пошук позицій, у яких результати відрізняються
error_positions = []

for i in range(len(decrypted_text)):
    if decrypted_text[i] != wrong_decrypted_text[i]:
        error_positions.append(i)

print("Кількість зіпсованих літер:", len(error_positions))
print("Перші 10 позицій з помилками:")
for pos in error_positions[:10]:
    print(
        "позиція:", pos,
        "| правильно:", decrypted_text[pos],
        "| з помилкою:", wrong_decrypted_text[pos]
    )

# Період між помилками
if len(error_positions) > 1:
    periods = []
    for i in range(1, len(error_positions)):
        periods.append(error_positions[i] - error_positions[i - 1])
    print("Період між помилками:", periods[:10])

# Виведення тексту
print("\nПерші 500 символів з правильним ключем:")
print(decrypted_text[:500])

print("\nПерші 500 символів з ключем з помилкою:")
print(wrong_decrypted_text[:500])
