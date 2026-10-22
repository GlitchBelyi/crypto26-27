# Використовує calc_h1 з lab1.py

import math
import random
import sys

from lab1 import calc_h1

N = 100_000  # довжина всіх послідовностей
SEED = 42
LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюяё"  # 33 літери

random.seed(SEED)


def run(text_path, alphabet, label):
    print(f"\n {label}: алфавіт = {len(alphabet)} символи, "
          f"H0 = log2({len(alphabet)}) = {math.log2(len(alphabet)):.4f} біт ")

    seqs = {}
    if text_path:
        with open(text_path, encoding="utf-8") as f:
            txt = f.read()
        if " " not in alphabet:
            txt = txt.replace(" ", "")
        seqs["А (природний текст)"] = txt[:N]
    seqs["Б (один символ)"] = alphabet[0] * N
    seqs["В (рівноймовірний random)"] = "".join(random.choices(alphabet, k=N))

    for name, s in seqs.items():
        h1 = abs(calc_h1(s)[0])  # abs прибирає "-0.0000" для Б
        print(f"  {name:28s} довжина = {len(s)}  H1 = {h1:.4f} біт/символ")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    run(path, LETTERS + " ", "З пробілом")
    run(path, LETTERS, "Без пробілу")