import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import h1, h2  # noqa: E402

LENGTH = 100_000  


def main():
    half = LENGTH // 2
    symbols = list("а" * half + "б" * half)
    random.shuffle(symbols)
    seq_g = "".join(symbols)
    seq_d = "аб" * half

    print(f"Довжина кожної послідовності: {LENGTH}\n")
    print(f"{'':<4}{'H1':>9}{'H2 перет.':>12}{'H2 неперет.':>14}")
    for label, seq in (("Г", seq_g), ("Д", seq_d)):
        print(f"{label:<4}{h1(seq):>9.4f}{h2(seq, True):>12.4f}{h2(seq, False):>14.4f}")


if __name__ == "__main__":
    main()