import sys, json
from collections import Counter
from vigenere import *
 
Y = load(sys.argv[1] if len(sys.argv) > 1 else "ciphertext_var2.txt")
n = len(Y)
res = {"n": n, "I_total": index_of_coincidence(Y), "I_theory": I_THEORY}
 

scan = []
for r in range(2, 31):
    scan.append((r, avg_block_ic(Y, r), coincidences(Y, r)))
res["scan"] = scan
print("r   avg I     D_r")
for r, a, d in scan:
    print(f"{r:<3} {a:.5f}  {d}")
 

thr = I_RANDOM + 0.75 * (I_THEORY - I_RANDOM)
cand = [r for r, a, d in scan if a > thr]
r_est = min(cand)
print("кандидати:", cand, "-> r =", r_est)
res["candidates"] = cand
res["r"] = r_est
res["threshold"] = thr
 

for r in sorted(set([7, 14, 21, 28])):
    print(r, [round(index_of_coincidence(b), 4) for b in blocks(Y, r)][:8], "...")
 

r = r_est
key_idx, table = [], []
for j, b in enumerate(blocks(Y, r)):
    top = Counter(b).most_common(3)
    heur = ALPHABET[(IDX[top[0][0]] - IDX["о"]) % M]         
    ms = sorted(((mutual_ic(b, g), g) for g in range(M)), reverse=True)
    key_idx.append(ms[0][1])
    table.append({
        "j": j, "L": len(b), "top3": [(c, k) for c, k in top], "heur": heur,
        "best": ALPHABET[ms[0][1]], "M1": ms[0][0],
        "second": ALPHABET[ms[1][1]], "M2": ms[1][0], "ic": index_of_coincidence(b),
    })
key = "".join(ALPHABET[k] for k in key_idx)
plain = decrypt(Y, key)
res.update(table=table, key=key, plain_ic=index_of_coincidence(plain),
           plain_head=plain[:300])
res["heur_key"] = "".join(t["heur"] for t in table)
print("ключ:", key, "| евристика:", res["heur_key"], "| I(відкр.) =", round(res["plain_ic"], 5))
open("decrypted.txt", "w", encoding="utf-8").write(plain)
 

pos, delta = 0, 1                       
bad_idx = key_idx[:]
bad_idx[pos] = (bad_idx[pos] + delta) % M
bad = "".join(ALPHABET[k] for k in bad_idx)
plain_bad = decrypt(Y, bad)
diff = [i for i in range(n) if plain[i] != plain_bad[i]]
shifts = Counter((IDX[plain_bad[i]] - IDX[plain[i]]) % M for i in diff)
res.update(bad_key=bad, n_diff=len(diff), diff_head=diff[:8],
           diff_step=sorted(set(diff[k + 1] - diff[k] for k in range(len(diff) - 1))),
           diff_shifts=dict(shifts), bad_head=plain_bad[:120], good_head=plain[:120],
           I_bad=index_of_coincidence(plain_bad),
           bad_cols_ic=[index_of_coincidence(b) for b in blocks(plain_bad, r)][:3])
print("спотворений ключ:", bad, "| змінено", len(diff), f"({len(diff)/n:.4%})",
      "| кроки:", res["diff_step"], "| зсуви:", dict(shifts))
print(plain[:70]); print(plain_bad[:70])
json.dump(res, open("results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)