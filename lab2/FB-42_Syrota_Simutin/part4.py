ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)

INPUT_FILE = "var4r.txt"
KEY = "громыковедьма"
POS = 4                       # номер символу ключа (з 0), який змінюємо
NEW = "н"                     # ы -> н

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read().strip()

def decrypt(t, key):
    return "".join(
        ALPHABET[(ALPHABET.index(c) - ALPHABET.index(key[i % len(key)])) % M]
        for i, c in enumerate(t)
    )

bad_key = KEY[:POS] + NEW + KEY[POS + 1:]
good = decrypt(text, KEY)
bad = decrypt(text, bad_key)

diff = [i for i in range(len(good)) if good[i] != bad[i]]
shift = (ALPHABET.index(NEW) - ALPHABET.index(KEY[POS])) % M

print("Правильний ключ:", KEY)
print("Хибний ключ:    ", bad_key)
print(f"Зсув у ключі: {shift}")
print(f"Всього літер: {len(good)}, змінилось: {len(diff)} ({len(diff)/len(good):.2%})")
print(f"Теоретично 1/13 = {1/13:.2%}")
print("Перші позиції змін:", diff[:8])
print("Різниці позицій:", sorted({diff[i+1]-diff[i] for i in range(len(diff)-1)}))
print()
print("Правильно:", good[:65])
print("З помилкою:", bad[:65])
print()
print("Заміна на позиціях змін (перші 5):")
for i in diff[:5]:
    d = (ALPHABET.index(good[i]) - ALPHABET.index(bad[i])) % M
    print(f"  позиція {i}: {good[i]} -> {bad[i]}  (зсув {d})")
