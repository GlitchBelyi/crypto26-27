import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (  # noqa: E402
    ALPHABET_WITH_SPACE, LETTERS, bigram_freqs, char_freqs, entropy,
    h0, read_text, redundancy, top_n,
)

DIR = Path(__file__).parent


def show(s):
    return s.replace(" ", "_")


def analyse(name, text, alphabet):
    print("=" * 60)
    print(f"  {name}")
    print("=" * 60)
    print(f"Довжина тексту:    {len(text):,} символів")
    print(f"Розмір алфавіту m: {len(alphabet)}")
    print(f"H0 = log2(m):      {h0(alphabet):.4f} біт/символ\n")
    chars = char_freqs(text)
    H1 = entropy(chars)
    print(f"H1 = {H1:.4f} біт/символ   (R = {redundancy(H1, alphabet):.4f})")
    print("ТОП-5 символів:")
    for ch, cnt, p in top_n(chars, 5):
        print(f"   '{show(ch)}'  {cnt:>9,}  p = {p:.6f}")

    result = {"H1": H1}
    for overlapping in (True, False):
        mode = "перетинні (зсув 1)" if overlapping else "неперетинні (зсув 2)"
        bigrams = bigram_freqs(text, overlapping)
        H_bg = entropy(bigrams)     
        H2 = H_bg / 2          
        result["H2_over" if overlapping else "H2_non"] = H2

        print(f"\n Біграми, {mode} ")
        print(f"Усього біграм:     {sum(bigrams.values()):,}")
        print(f"Різних біграм:     {len(bigrams):,} з {len(alphabet) ** 2} можливих")
        print(f"H(біграми)       = {H_bg:.4f} біт/біграму")
        print(f"H2 = H(біграми)/2= {H2:.4f} біт/символ   (R = {redundancy(H2, alphabet):.4f})")
        print("ТОП-5 біграм:")
        for bg, cnt, p in top_n(bigrams, 5):
            print(f"   '{show(bg)}'  {cnt:>9,}  p = {p:.6f}")
    print()
    return result


def freq_table(text):
    counts = char_freqs(text)
    total = sum(counts.values())
    print(f"{'символ':>8} {'кількість':>11} {'частота':>10}")
    for ch, cnt in counts.most_common():
        print(f"{show(ch):>8} {cnt:>11,} {cnt / total:>10.6f}")


def main():
    with_space = read_text(DIR / "normalized_with_space.txt")
    no_space = read_text(DIR / "normalized_no_space.txt")

    a = analyse("ТЕКСТ ІЗ ПРОБІЛАМИ (алфавіт 33)", with_space, ALPHABET_WITH_SPACE)
    b = analyse("ТЕКСТ БЕЗ ПРОБІЛІВ (алфавіт 32)", no_space, LETTERS)

    print("=" * 60)
    print("  ЗВЕДЕНА ТАБЛИЦЯ (біт/символ)")
    print("=" * 60)
    print(f"{'варіант':<20}{'H1':>9}{'H2 перет.':>12}{'H2 неперет.':>14}")
    for label, r in (("з пробілами", a), ("без пробілів", b)):
        print(f"{label:<20}{r['H1']:>9.4f}{r['H2_over']:>12.4f}{r['H2_non']:>14.4f}")

    print("\n" + "=" * 60)
    print("  ТАБЛИЦЯ ЧАСТОТ СИМВОЛІВ (текст із пробілами)")
    print("=" * 60)
    freq_table(with_space)


if __name__ == "__main__":
    main()