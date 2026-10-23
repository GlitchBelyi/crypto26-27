from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
KEY = "возвращениеджинна"
POS = 6                    
NEW = "ч"                  
 
def main():
    y = clean(open("cipher_variant6.txt", encoding="utf-8").read())
    n, r = len(y), len(KEY)
    good = decrypt(y, KEY)
    bad_key = KEY[:POS] + NEW + KEY[POS + 1:]
    bad = decrypt(y, bad_key)
 
    delta = (IDX[NEW] - IDX[KEY[POS]]) % M    
    shift = (-delta) % M                       
    n_pos = len(range(POS, n, r))
 
    print("ПРОГНОЗ (до експерименту)")
    print(f"  правильний ключ: {KEY}")
    print(f"  змінений ключ:   {bad_key}   (позиція {POS}: «{KEY[POS]}» -> «{NEW}», Δk = {delta} mod {M})")
    print(f"  зміняться лише символи з номерами i = {POS} (mod {r}) -> {n_pos} з {n} = {n_pos / n:.2%}")
    print(f"  усі вони зсунуться на одну величину -Δk = {shift} (mod {M}); решта тексту не зміниться")
 
    diff = [i for i in range(n) if good[i] != bad[i]]
    shifts = {(IDX[bad[i]] - IDX[good[i]]) % M for i in diff}
    print("\nРЕЗУЛЬТАТ")
    print(f"  відмінностей: {len(diff)} з {n} ({len(diff) / n:.2%})")
    print(f"  усі відмінності при i mod {r} = {POS}: {all(i % r == POS for i in diff)}")
    print(f"  множина зсувів спотворених символів: {shifts}")
    print(f"  I(правильний) = {index_of_coincidence(good):.5f}, I(зі змінним ключем) = {index_of_coincidence(bad):.5f}")
    print("  приклади замін:", ", ".join(f"{good[i]}->{bad[i]}" for i in diff[:12]))
    print("\n  Текст рядками по 17 символів (стовпець = позиція ключа; ^ = спотворений стовпець):")
    print("    " + "".join(" " if j != POS else "^" for j in range(r)))
    for row in range(5):
        print("    " + good[row * r:(row + 1) * r] + " правильно")
        print("    " + bad[row * r:(row + 1) * r] + "  зі зміненим ключем")
    print("\nПочаток тексту:")
    print("  правильно:", good[:90])
    print("  помилково:", bad[:90])
    print("\nЧастка спотворених символів за позиціями:")
    fr = []
    for p in range(r):
        k2 = KEY[:p] + ("б" if KEY[p] == "а" else "а") + KEY[p + 1:]
        d = sum(1 for a, b in zip(good, decrypt(y, k2)) if a != b)
        fr.append(d / n)
    print("  " + " ".join(f"{p}:{v:.3f}" for p, v in enumerate(fr)))

if __name__ == "__main__":
    main()