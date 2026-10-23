from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
R_MAX = 40                 
CANDIDATES = [34, 4, 28, 40, 16, 18]   
OWN_KEYS = ["ян", "сад", "луна", "весна", "криптография", "защитаинформациисети"]
 
def main():
    y = clean(open("cipher_variant6.txt", encoding="utf-8").read())
    n = len(y)
    i_y = index_of_coincidence(y)
    print(f"Довжина шифртексту n = {n}")
    print(f"I(ШТ) = {i_y:.5f}   (I0 = {I_RANDOM:.5f}, I мови = {I_LANG:.5f})")
 
    plain = clean(open("plain_raw.txt", encoding="utf-8").read())
    print("\nПорівняння з індексами власних шифртекстів")
    print("  ключ                     r    I_r     |I_r - I(ШТ)|")
    for k in OWN_KEYS:
        ir = index_of_coincidence(encrypt(plain, k))
        print(f"  {k:<22}{len(k):>3}  {ir:.5f}   {abs(ir - i_y):.5f}")
    thr = (I_LANG + I_RANDOM) / 2
    print(f"\n  r   сер. I   D(r)   D(r)/(n-r)   довж. блока")
    rows = []
    for r in range(1, R_MAX + 1):
        ai, d = avg_block_ic(y, r), d_stat(y, r)
        rows.append((r, ai, d, d / (n - r), n // r))
        mark = "  <== пік" if ai > thr else ""
        print(f"{r:>3}   {ai:.5f}  {d:>4}   {d / (n - r):.5f}     {n // r:>6}{mark}")
    peaks = [r for r, ai, *_ in rows if ai > thr]
    print(f"\nПоріг (I мови + I0)/2 = {thr:.5f}; піки при r = {peaks}")
    if peaks:
        base = min(peaks)
        print(f"Найменше r з піком: {base}; решта піків кратні йому: "
              f"{all(p % base == 0 for p in peaks)}")
    print("\nДеталі по кандидатах (I кожного блока; скільки блоків ближче до I мови, ніж до I0)")
    for r in [min(peaks) if peaks else 17] + CANDIDATES:
        bl = [index_of_coincidence(b) for b in blocks(y, r)]
        close = sum(1 for v in bl if abs(v - I_LANG) < abs(v - I_RANDOM))
        d = d_stat(y, r)
        print(f"r={r:>2}  блок={n // r:>4}  сер.I={sum(bl) / r:.5f}  D/(n-r)={d / (n - r):.5f}  "
              f"I блоків: {min(bl):.5f}..{max(bl):.5f}  ближче до I мови: {close}/{r}")

if __name__ == "__main__":
    main()