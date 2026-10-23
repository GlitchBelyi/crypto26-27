INPUT_FILE = "var4r.txt"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    text = file.read().strip()

n = len(text)

print(f"Довжина шифртексту: {n}")
print()

print(" r    D_r")
print("-" * 15)

for r in range(2, 31):
    matches = 0

    for i in range(n - r):
        if text[i] == text[i + r]:
            matches += 1

    print(f"{r:2}    {matches}")