from collections import Counter
from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
KEYS = ["ян", "сад", "луна", "весна", "криптография", "защитаинформациисети"]
 
def main():
    with open("plain_raw.txt", encoding="utf-8") as f:
        raw = f.read()
    plain = clean(raw)
    print(f"Розмір вихідного файла: {len(raw.encode('utf-8'))} байт (UTF-8)")
    print(f"Довжина ВТ після очищення: {len(plain)} символів")
 
    cnt = Counter(plain)
    print("\nлітера   частота мови   частота ВТ")
    for c in FREQ_ORDER:
        print(f"  {c}       {FREQ[c]:.5f}        {cnt.get(c, 0) / len(plain):.5f}")
    print(f"\nТеоретичний I мови = {I_LANG:.5f}, I0 = 1/m = {I_RANDOM:.5f}")
 
    print("\nКлюч                      r      I")
    print(f"(відкритий текст)         -   {index_of_coincidence(plain):.5f}")
    for k in KEYS:
        ct = encrypt(plain, k)
        assert decrypt(ct, k) == plain          
        print(f"{k:<24}{len(k):>3}   {index_of_coincidence(ct):.5f}")
        print("    " + ct[:70])
if __name__ == "__main__":
    main()