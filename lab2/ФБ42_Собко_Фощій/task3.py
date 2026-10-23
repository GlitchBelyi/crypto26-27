from collections import Counter
from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = 17
def key_symbol(block, x_star):
    y_star, n_star = Counter(block).most_common(1)[0]
    return y_star, n_star, ALPHABET[(IDX[y_star] - IDX[x_star]) % M]
 
def mutual_index(block, g):
    cnt = Counter(block)
    return sum(FREQ[ALPHABET[t]] * cnt.get(ALPHABET[(t + g) % M], 0) for t in range(M)) / len(block)
 
def main():
    y = clean(open("cipher_variant6.txt", encoding="utf-8").read())
    bl = blocks(y, R)

    print("Крок 1. y* -> x* = «о»")
    print("  фр.  y*  N(y*)   k(о)   топ-3 літери блока")
    base = ""
    for i, b in enumerate(bl):
        ys, ny, k = key_symbol(b, "о")
        base += k
        top3 = " ".join(f"{c}:{n}" for c, n in Counter(b).most_common(3))
        print(f"  {i:>2}   {ys}   {ny:>3}    {k}     {top3}")
    print("\nКлюч за x* = «о»:", base)
    print("Текст:", decrypt(y, base)[:120])
    print("\nКрок 2. Перевірка: найкращі зсуви за M_g (для кожного блока)")
    final = ""
    bad = []
    for i, b in enumerate(bl):
        ranked = sorted(range(M), key=lambda g: -mutual_index(b, g))
        best = ranked[0]
        final += ALPHABET[best]
        if ALPHABET[best] != base[i]:
            bad.append(i)
        print(f"  фр.{i:>2}: " + "  ".join(f"{ALPHABET[g]}={mutual_index(b, g):.4f}" for g in ranked[:3]),
              "  <-- не збігається з x*=«о»" if ALPHABET[best] != base[i] else "")
    print(f"\nКрок 3. Блоки, де x* = «о» для найчастішого y* не спрацювало: {bad}")
    for i in bad:
        b = bl[i]
        top_y = Counter(b).most_common(3)
        print(f"\n  Фрагмент {i}: найчастіші літери " + ", ".join(f"{c}:{n}" for c, n in top_y))
        cands = {}
        for yc, ny in top_y:
            for x in "оеа":
                k = ALPHABET[(IDX[yc] - IDX[x]) % M]
                cands.setdefault(k, []).append(f"y*={yc},x*={x}")
        ranked = sorted(cands, key=lambda k: -mutual_index(b, IDX[k]))
        print("    k    M_g     походження              початок розшифрованого тексту")
        for k in ranked[:4]:
            trial = base[:i] + k + base[i + 1:]
            trial = "".join(final[j] if j != i and j in bad else trial[j] for j in range(R))
            seg = decrypt(y, trial)[:50]
            print(f"    {k}   {mutual_index(b, IDX[k]):.4f}   {'; '.join(cands[k]):<22}  {seg}")

    print("\nВідновлений ключ:", final)
    plain = decrypt(y, final)
    print(f"I(розшифр.) = {index_of_coincidence(plain):.5f}  (I мови = {I_LANG:.5f})")
    print(f"Довжина: {len(plain)}")
    print("\nРозшифрований текст:\n" + plain)
    with open("decrypted_variant6.txt", "w", encoding="utf-8") as f:
        f.write(plain + "\n")
 
if __name__ == "__main__":
    main()