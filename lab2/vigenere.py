import re
from collections import Counter
 
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
IDX = {c: i for i, c in enumerate(ALPHABET)}

 
_RAW = {
    'о': 0.1112, 'е': 0.0861, 'а': 0.0829, 'и': 0.0706, 'н': 0.0642, 'т': 0.0598,
    'с': 0.0538, 'л': 0.0494, 'в': 0.0468, 'р': 0.0465, 'к': 0.0355, 'д': 0.0326,
    'м': 0.0309, 'у': 0.0289, 'п': 0.0285, 'я': 0.0202, 'г': 0.0195, 'ь': 0.0185,
    'ы': 0.0177, 'з': 0.0173, 'б': 0.0169, 'ч': 0.0152, 'й': 0.0125, 'ж': 0.0112,
    'ш': 0.0089, 'х': 0.0088, 'ю': 0.0062, 'ц': 0.0038, 'щ': 0.0034, 'э': 0.0030,
    'ф': 0.0022, 'ъ': 0.0004,
}

_S = sum(_RAW.values())
P = [_RAW[c] / _S for c in ALPHABET]         
I_THEORY = sum(p * p for p in P)              
I_RANDOM = 1.0 / M                           
 

def clean(text: str) -> str:
    text = text.lower().replace("ё", "е")
    return "".join(ch for ch in text if ch in IDX)
 
 
def load(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        lines = f.read().lower().splitlines()
    if lines and "ариант" in lines[0]:
        lines = lines[1:]
    return clean("".join(lines))
 
 
def shift(text: str, key: str, sign: int) -> str:
    r = len(key)
    return "".join(
        ALPHABET[(IDX[ch] + sign * IDX[key[i % r]]) % M] for i, ch in enumerate(text)
    )
 
 
def encrypt(text: str, key: str) -> str:
    return shift(text, clean(key), +1)
 
 
def decrypt(text: str, key: str) -> str:
    return shift(text, clean(key), -1)
 
 
def index_of_coincidence(text: str) -> float:
    n = len(text)
    if n < 2:
        return 0.0
    return sum(v * (v - 1) for v in Counter(text).values()) / (n * (n - 1))
 
 
def blocks(text: str, r: int):
    return [text[j::r] for j in range(r)]
 
 
def avg_block_ic(text: str, r: int) -> float:
    b = blocks(text, r)
    return sum(index_of_coincidence(x) for x in b) / r
 
 
def coincidences(text: str, r: int) -> int:
    return sum(text[i] == text[i + r] for i in range(len(text) - r))
 
 
def mutual_ic(block: str, g: int) -> float:
    L = len(block)
    c = Counter(block)
    return sum(c.get(ALPHABET[t], 0) / L * P[(t - g) % M] for t in range(M))
 