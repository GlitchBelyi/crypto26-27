import csv
import random
import matplotlib.pyplot as plt
from vigenere import A, ARTIFACTS, M, RESULTS, encrypt, index_of_coincidence, load, save_json, theoretical_index

KEYS = ["ум", "дом", "море", "школа", "защитаинформации"]
RANDOM_R = range(1, 31)
KEYS_PER_R = 100

x = load("plaintext.txt")
i_plain = index_of_coincidence(x)
print(f"Довжина ВТ: {len(x)}, I(ВТ) = {i_plain:.5f}, I теор. = {theoretical_index():.5f}, I0 = {1 / M:.5f}")

rows = []
for key in KEYS:
    ic = index_of_coincidence(encrypt(x, key))
    rows.append({"key": key, "r": len(key), "ic": ic})
    print(f"r = {len(key):2d}  ключ = {key:18s}  I(ШТ) = {ic:.5f}")

random.seed(2)
curve = []
for r in RANDOM_R:
    vals = [index_of_coincidence(encrypt(x, "".join(random.choices(A, k=r)))) for _ in range(KEYS_PER_R)]
    curve.append({"r": r, "mean": sum(vals) / len(vals), "min": min(vals), "max": max(vals)})

with open(RESULTS / "task1_ic.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ключ", "r", "I"])
    w.writerow(["(відкритий текст)", 0, f"{i_plain:.5f}"])
    w.writerows([[d["key"], d["r"], f"{d['ic']:.5f}"] for d in rows])

with open(RESULTS / "task1_random_keys.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["r", "I_сер", "I_мін", "I_макс"])
    w.writerows([[d["r"], f"{d['mean']:.5f}", f"{d['min']:.5f}", f"{d['max']:.5f}"] for d in curve])

save_json("task1.json", {"n": len(x), "i_plain": i_plain, "i_theor": theoretical_index(),
                         "keys": rows, "curve": curve, "keys_per_r": KEYS_PER_R})

rs = [d["r"] for d in curve]
plt.figure(figsize=(7, 4))
plt.fill_between(rs, [d["min"] for d in curve], [d["max"] for d in curve], alpha=0.25, label="мін–макс")
plt.plot(rs, [d["mean"] for d in curve], marker="o", ms=3, label="середнє")
plt.axhline(i_plain, color="g", ls="--", label="I відкритого тексту")
plt.axhline(1 / M, color="r", ls="--", label="I₀ = 1/32")
plt.xlabel("довжина ключа r")
plt.ylabel("індекс відповідності")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(ARTIFACTS / "task1_ic_vs_r.png", dpi=200)
