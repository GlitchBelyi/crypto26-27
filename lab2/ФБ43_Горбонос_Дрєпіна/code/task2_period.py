import csv
import json
import matplotlib.pyplot as plt
from vigenere import (ARTIFACTS, M, RESULTS, avg_block_ic, coincidences, decrypt, index_of_coincidence, load,
                      recover_key, save_json, split_blocks, theoretical_index)

R_MAX = 40
CANDIDATES = [7, 14, 21, 28, 35]

y = load("variant2_cipher.txt")
n = len(y)
i_y = index_of_coincidence(y)
i_lang = theoretical_index()
print(f"n = {n}, I(Y) = {i_y:.5f}, I теор. = {i_lang:.5f}, I0 = {1 / M:.5f}\n")

ref = {}
ref_path = RESULTS / "task1.json"
if ref_path.exists():
    ref = {d["r"]: d["mean"] for d in json.load(open(ref_path, encoding="utf-8"))["curve"]}

table = []
print(" r   I_сер    I_мін    I_макс    D_r   D_r/(n-r)")
for r in range(2, R_MAX + 1):
    ics = [index_of_coincidence(b) for b in split_blocks(y, r)]
    d = coincidences(y, r)
    row = {"r": r, "avg": sum(ics) / r, "min": min(ics), "max": max(ics), "d": d, "d_norm": d / (n - r)}
    table.append(row)
    print(f"{r:2d}   {row['avg']:.5f}  {row['min']:.5f}  {row['max']:.5f}   {d:4d}   {row['d_norm']:.4f}")

with open(RESULTS / "task2_period.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["r", "I_сер", "I_мін", "I_макс", "D_r", "D_r/(n-r)"])
    w.writerows([[t["r"], f"{t['avg']:.5f}", f"{t['min']:.5f}", f"{t['max']:.5f}", t["d"], f"{t['d_norm']:.4f}"] for t in table])

best_avg = max(t["avg"] for t in table)
peak_r = [t["r"] for t in table if t["avg"] >= 0.9 * best_avg]
background = sorted(t["d"] for t in table)[len(table) // 2]
peak_d = [t["r"] for t in table if t["d"] >= 1.4 * background]
print(f"\nr з I_сер ≥ 0.9·max: {peak_r}\nмедіана D_r = {background}, r з D_r ≥ 1.4·медіани: {peak_d}")
print(f"Другий алгоритм: I(Y) = {i_y:.5f}; найближчі еталонні r: "
      f"{sorted(ref, key=lambda r: abs(ref[r] - i_y))[:5] if ref else 'немає task1.json'}")

cands = []
print("\nr    I_сер    I_мін    I_макс   I(розш.)  ключ")
for r in CANDIDATES:
    ics = [index_of_coincidence(b) for b in split_blocks(y, r)]
    key = recover_key(y, r)
    x = decrypt(y, key)
    cands.append({"r": r, "avg": sum(ics) / r, "min": min(ics), "max": max(ics), "key": key,
                  "ic_dec": index_of_coincidence(x), "sample": x[:50]})
    print(f"{r:2d}   {cands[-1]['avg']:.5f}  {cands[-1]['min']:.5f}  {cands[-1]['max']:.5f}   "
          f"{cands[-1]['ic_dec']:.5f}   {key}   {x[:30]}")

save_json("task2.json", {"n": n, "i_y": i_y, "i_lang": i_lang, "table": table, "candidates": cands,
                         "peak_r": peak_r, "peak_d": peak_d, "median_d": background,
                         "ref": {str(k): v for k, v in ref.items()}})

rs = [t["r"] for t in table]
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].bar(rs, [t["avg"] for t in table], color="#4C72B0")
ax[0].axhline(i_lang, color="g", ls="--", label="I мови")
ax[0].axhline(1 / M, color="r", ls="--", label="I₀ = 1/32")
ax[0].set_xlabel("r")
ax[0].set_ylabel("середній I блоків")
ax[0].legend(loc="upper left", fontsize=8)
ax[1].bar(rs, [t["d"] for t in table], color="#DD8452")
ax[1].set_xlabel("r")
ax[1].set_ylabel("$D_r$")
for a in ax:
    a.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(ARTIFACTS / "task2_period.png", dpi=200)
