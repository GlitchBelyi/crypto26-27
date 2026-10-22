# Використовує calc_h1 та calc_h2_* з lab1.py

import random
from collections import Counter

from lab1 import calc_h1, calc_h2_overlapping, calc_h2_non_overlapping

N = 100_000
SEED = 42
LETTERS = "абвгдежзийклмнопрстуфхцчшщъыьэюяё"

random.seed(SEED)


def run(alphabet, label):
    print(f"\n {label} (алфавіт '{alphabet}') ")
    k = len(alphabet)

    # Д - символи утв. виражену періодичну структуру (ababab...)
    d = (alphabet * (N // k + 1))[:N]

    # Г - символи розташовані у випадковому порядку
    letters = list(d)
    random.shuffle(letters)
    g = "".join(letters)

    assert Counter(g) == Counter(d), "частоти символів мають збігатися"

    for name, s in (("Г (випадковий порядок)", g), ("Д (періодична)", d)):
        h1 = abs(calc_h1(s)[0])
        h2_ov = abs(calc_h2_overlapping(s)[0])
        h2_nov = abs(calc_h2_non_overlapping(s)[0])
        print(f"  {name:24s} H1 = {h1:.4f}  "
              f"H2 (перетин.) = {h2_ov:.4f}  H2 (неперетин.) = {h2_nov:.4f}")


if __name__ == "__main__":
    run("ab", "Період 2")
    run("abcd", "Період 4")
    run(LETTERS, "Весь алфавіт, період 33")