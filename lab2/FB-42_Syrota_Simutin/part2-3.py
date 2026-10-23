from collections import Counter

INPUT_FILE = "var4r.txt"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read().strip()

def coincidence_index(t):
    n = len(t)
    f = Counter(t)
    return sum(c * (c - 1) for c in f.values()) / (n * (n - 1))

print(f"Довжина шифртексту: {len(text)}")
print(f"Індекс відповідності всього шифртексту: {coincidence_index(text):.6f}")
print()
print(" r    середній I(Y_i)")
print("-" * 22)

for r in range(1, 31):
    blocks = [text[i::r] for i in range(r)]
    avg = sum(coincidence_index(b) for b in blocks) / r
    print(f"{r:2}    {avg:.6f}")
