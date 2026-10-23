import sys
from vigenere import IDX, M, RESULTS, decrypt, index_of_coincidence, load, save_json

KEY = (RESULTS / "task3_key.txt").read_text(encoding="utf-8").strip()
CASES = [(3, "в"), (6, "м"), (0, "а")]

if len(sys.argv) == 3:
    CASES = [(int(sys.argv[1]), sys.argv[2])]

y = load("variant2_cipher.txt")
x = decrypt(y, KEY)
r = len(KEY)
out = []

for pos, new in CASES:
    bad_key = KEY[:pos] + new + KEY[pos + 1:]
    xb = decrypt(y, bad_key)
    diff = [i for i in range(len(x)) if x[i] != xb[i]]
    shifts = {(IDX[xb[i]] - IDX[x[i]]) % M for i in diff}
    steps = sorted({b - a for a, b in zip(diff, diff[1:])})
    out.append({"pos": pos, "old": KEY[pos], "new": new, "bad_key": bad_key, "changed": len(diff), "n": len(x),
                "share_ok": 1 - len(diff) / len(x), "first": diff[:6], "steps": steps, "shifts": sorted(shifts),
                "expected_shift": (IDX[KEY[pos]] - IDX[new]) % M, "ic": index_of_coincidence(xb),
                "sample_ok": x[:60], "sample_bad": xb[:60]})
    d = out[-1]
    print(f"Позиція {pos}: {d['old']} -> {new}, ключ {bad_key}")
    print(f"  змінено {d['changed']} з {d['n']} ({1 - d['share_ok']:.4f}), очікувано n/r = {len(x) / r:.1f}")
    print(f"  перші позиції {d['first']}, крок {steps}")
    print(f"  зсув літер: {d['shifts']} (очікувано {d['expected_shift']}), I(X') = {d['ic']:.5f}")
    print(f"  {d['sample_ok']}\n  {d['sample_bad']}\n")

save_json("task4.json", {"key": KEY, "ic_ok": index_of_coincidence(x), "cases": out})
with open(RESULTS / "task4_experiment.txt", "w", encoding="utf-8") as f:
    for d in out:
        f.write(f"позиція {d['pos']}: {d['old']} -> {d['new']}; змінено {d['changed']} з {d['n']}; "
                f"крок {d['steps']}; зсув {d['shifts']}; I = {d['ic']:.5f}\n")
