import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import LETTERS  # noqa: E402

DIR = Path(__file__).parent
SRC_FILE = DIR / "bratia_karamazovy.txt" 

LETTER_SET = set(LETTERS)


def normalize(raw):
    out = []
    prev_space = True  
    for ch in raw.lower():
        if ch == "ё":
            ch = "е"
        if ch in LETTER_SET:
            out.append(ch)
            prev_space = False
        elif not prev_space:
            out.append(" ")
            prev_space = True
    return "".join(out).rstrip()


def main(src_path):
    raw = Path(src_path).read_text(encoding="cp1251")
    with_space = normalize(raw)
    no_space = with_space.replace(" ", "")

    (DIR / "normalized_with_space.txt").write_text(with_space, encoding="utf-8")
    (DIR / "normalized_no_space.txt").write_text(no_space, encoding="utf-8")

    print(f"Вихідний файл:             {src_path}")
    print(f"Довжина сирого тексту: {len(raw)}")
    print(f"Довжина після нормалізації (з пробілами): {len(with_space)}")
    print(f"Довжина без пробілів: {len(no_space)}")
    print("Перші 300 символів після обробки:")
    print(with_space[:300])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else SRC_FILE)