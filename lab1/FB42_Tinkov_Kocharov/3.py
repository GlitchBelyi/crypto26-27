import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import LETTERS, h1, read_text 

DIR = Path(__file__).parent
LENGTH = 100_000   


def main():
    seq_a = read_text(DIR / "normalized_no_space.txt")[:LENGTH]
    seq_b = "а" * LENGTH
    seq_v = "".join(random.choice(LETTERS) for _ in range(LENGTH))

    print(f"Довжина кожної послідовності: {LENGTH}\n")
    print(f"А — фрагмент природного тексту:   H1 = {h1(seq_a):.4f}")
    print(f"Б — повторення одного символу:    H1 = {h1(seq_b):.4f}")
    print(f"В — рівноймовірна випадкова:      H1 = {h1(seq_v):.4f}")


if __name__ == "__main__":
    main()