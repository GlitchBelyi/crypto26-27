import re, math, sys
from collections import Counter
from itertools import permutations

ALPHA = "абвгдежзийклмнопрстуфхцчшщьыэюя"  # 31 літера (ё->е, ъ->ь)
M = len(ALPHA); M2 = M*M
IDX = {c:i for i,c in enumerate(ALPHA)}

def read_text(path):
    t = open(path, encoding="utf-8").read().lower()
    return "".join(c for c in t if c in IDX)

def egcd(a, b):
    u0, u1, v0, v1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q*b
        u0, u1 = u1, u0 - q*u1
        v0, v1 = v1, v0 - q*v1
    return a, u0, v0

def inv(a, n):
    g, u, _ = egcd(a % n, n)
    return u % n if g == 1 else None

def solve_lin(a, b, n):
    a %= n; b %= n
    d, _, _ = egcd(a, n)
    if b % d: return []
    a1, b1, n1 = a//d, b//d, n//d
    x0 = (b1 * inv(a1, n1)) % n1 if n1 > 1 else 0
    return [x0 + k*n1 for k in range(d)]

def bigrams_nonoverlap(t):
    return [t[i:i+2] for i in range(0, len(t)-1, 2)]

def top_bigrams(t, k=5):
    return Counter(bigrams_nonoverlap(t)).most_common(k)

def bg2num(bg): return IDX[bg[0]]*M + IDX[bg[1]]
def num2bg(x): return ALPHA[x//M] + ALPHA[x%M]

def decrypt(ct, a, b):
    ai = inv(a, M2)
    out = []
    for bg in bigrams_nonoverlap(ct):
        X = (ai * (bg2num(bg) - b)) % M2
        out.append(num2bg(X))
    return "".join(out)

# ---- розпізнавач мови ----
FORBIDDEN = ["аь","оь","иь","еь","уь","юь","яь","ьь","жы","шы","чы","щы","чя",
             "щя","чю","щю","йь","ыь","ьы","ьа","ьо","ьу","ьи","ьэ"]

def score(t):
    n = len(t)
    c = Counter(t)
    f_common = sum(c[x] for x in "оеа")/n           # у мові ~0.27
    f_rare = sum(c[x] for x in "фщь")/n              # у мові ~0.03
    bad = sum(t.count(f) for f in FORBIDDEN)/n       # забороненіі біграми
    return f_common, f_rare, bad

def is_meaningful(t):
    fc, fr, bad = score(t)
    return fc > 0.22 and fr < 0.06 and bad < 0.005
    
RU_TOP = ["ст","но","то","на","ен"]

def attack(ct, verbose=True, topn=5):
    cb = [bg for bg,_ in top_bigrams(ct, topn)]
    Xs = [bg2num(b) for b in RU_TOP]
    Ys = [bg2num(b) for b in cb]
    found = []
    tried = 0
    for i, j in permutations(range(5), 2):        # X*,X**
        for k, l in permutations(range(5), 2):    # Y*,Y**
            dx = (Xs[i]-Xs[j]) % M2
            dy = (Ys[k]-Ys[l]) % M2
            for a in solve_lin(dx, dy, M2):
                if egcd(a, M2)[0] != 1: continue
                b = (Ys[k] - a*Xs[i]) % M2
                tried += 1
                pt = decrypt(ct, a, b)
                if is_meaningful(pt):
                    found.append((a, b, RU_TOP[i], RU_TOP[j], cb[k], cb[l], pt))
    return found, tried

ORDERS = ["абвгдежзийклмнопрстуфхцчшщьыэюя", "абвгдежзийклмнопрстуфхцчшщыьэюя"]

def set_alphabet(al):
    global ALPHA, IDX
    ALPHA = al
    IDX = {c: i for i, c in enumerate(al)}

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "v3_test.utf-8.txt"
    for al in ORDERS:
        set_alphabet(al)
        ct = read_text(path)
        res, tried = attack(ct)
        if not res:
            continue
        print("алфавіт:", al)
        print("довжина:", len(ct), "букв;", "топ-5 біграм шифртексту:", top_bigrams(ct))
        print("перевірено кандидатів:", tried, "; пройшли критерій:", len(res))
        a, b = res[0][:2]
        print(f"ключ: a={a}, b={b}, a^-1={inv(a, M2)}")
        print(res[0][6][:300])
        open(path.rsplit('.',1)[0] + "_decrypted.txt", "w", encoding="utf-8").write(res[0][6])
        break
    else:
        print("ключ не знайдено")
