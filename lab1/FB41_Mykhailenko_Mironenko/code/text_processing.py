from pathlib import Path


RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_WITH_SPACE = RUSSIAN_LETTERS + " "


def russian_text_score(text):
    text = text.lower()

    common = [
        " и ",
        " в ",
        " не ",
        " на ",
        " что ",
        " как ",
        " это ",
    ]

    return sum(text.count(word) for word in common)


def read_text_auto(path: Path):
    raw = path.read_bytes()

    for encoding in ("utf-8-sig", "utf-8"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            pass

    variants = []

    for encoding in ("cp1251", "koi8-r"):
        try:
            text = raw.decode(encoding)
            variants.append(
                (russian_text_score(text), text, encoding)
            )
        except UnicodeDecodeError:
            pass

    if not variants:
        raise ValueError("Не вдалося прочитати файл.")

    _, text, encoding = max(variants)

    return text, encoding


def normalize_text(text):
    letters = set(RUSSIAN_LETTERS)

    text = text.lower()

    text = "".join(
        char if char in letters else " "
        for char in text
    )

    return " ".join(text.split())