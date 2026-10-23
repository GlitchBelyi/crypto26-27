import csv
import sys
from collections import Counter
import matplotlib.pyplot as plt
from vigenere import (A, ARTIFACTS, FREQ, IDX, M, RESULTS, decrypt, index_of_coincidence, load, recover_key,
                      save_json, shift_by_freq, shift_by_letter, split_blocks)

r = int(sys.argv[1]) if len(sys.argv) > 1 else 14
y = load("variant2_cipher.txt")
key = recover_key(y, r)

rows = []
print(" i    N   топ-3 літери блока        k(о)  k(част.)  літера для 'о'-зсуву: місце  найчастіша -> ВТ")
for i, block in enumerate(split_blocks(y, r)):
    cnt = Counter(block)
    ranked = [c for c, _ in cnt.most_common()]
    top = cnt.most_common(3)
    k_o, k_f = A[shift_by_letter(block)], A[shift_by_freq(block)]
    image_of_o = A[(IDX["о"] + IDX[key[i]]) % M]
    rank = ranked.index(image_of_o) + 1
    top_plain = A[(IDX[top[0][0]] - IDX[key[i]]) % M]
    rows.append({"i": i, "n": len(block), "top": top, "k_o": k_o, "k_f": k_f, "image_o": image_of_o,
                 "rank": rank, "top_plain": top_plain})
    print(f"{i:2d}  {len(block)}   " + ", ".join(f"{c}:{v}" for c, v in top).ljust(24) +
          f"  {k_o}     {k_f}        {image_of_o}: {rank}   {top[0][0]} -> {top_plain}")

x = decrypt(y, key)
wrong_o = [i for i, d in enumerate(rows) if d["k_o"] != d["k_f"]]
dec_top = Counter(x).most_common(6)
print(f"\nКлюч: {key}\nI(Y) = {index_of_coincidence(y):.5f}, I(X) = {index_of_coincidence(x):.5f}")
print(f"Блоки, де k(о) хибний: {wrong_o}")
print("Найчастіші літери в X:", ", ".join(f"{c}:{v / len(x):.4f}" for c, v in dec_top))
print(x[:300])

(RESULTS / "task3_key.txt").write_text(key, encoding="utf-8")
(RESULTS / "decrypted.txt").write_text(x, encoding="utf-8")
with open(RESULTS / "task3_blocks.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["i", "N", "топ-1", "топ-2", "топ-3", "k(о)", "k(част.)", "образ о", "місце", "найчастіша -> ВТ"])
    for d in rows:
        w.writerow([d["i"], d["n"]] + [f"{c}:{v}" for c, v in d["top"]] +
                   [d["k_o"], d["k_f"], d["image_o"], d["rank"], f"{d['top'][0][0]}->{d['top_plain']}"])

dec_freq = {c: v / len(x) for c, v in Counter(x).items()}
save_json("task3.json", {"r": r, "key": key, "blocks": rows, "wrong_o": wrong_o, "ic_y": index_of_coincidence(y),
                         "ic_x": index_of_coincidence(x), "top_dec": dec_top, "n": len(x), "sample": x[:300],
                         "dec_freq": dec_freq})

block0 = Counter(split_blocks(y, r)[0])
n0 = sum(block0.values())
shifted = [block0.get(A[(t + IDX[key[0]]) % M], 0) / n0 for t in range(M)]
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
ax[0].bar(list(A), [block0.get(c, 0) / n0 for c in A], color="#4C72B0")
ax[0].set_title("Частоти літер блока Y₀ (шифртекст)")
ax[1].bar(list(A), shifted, color="#55A868", label=f"Y₀ зсунутий на k₀ = '{key[0]}'")
ax[1].plot(list(A), [FREQ[c] for c in A], "ro", ms=3, label="частоти мови")
ax[1].set_title("Після зсуву на знайдений ключ")
ax[1].legend(fontsize=8)
for a in ax:
    a.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(ARTIFACTS / "task3_block0.png", dpi=200)
