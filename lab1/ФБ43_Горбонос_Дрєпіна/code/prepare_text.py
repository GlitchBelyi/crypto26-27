import html
import re
import sys
import urllib.request
from pathlib import Path

URL = "http://az.lib.ru/t/tolstoj_lew_nikolaewich/text_0080.shtml"
MERGE_HARD_SIGN = True  # True: 31 літера (ё->е, ъ->ь); False: 32 літери (лише ё->е)
START_MARK = "все счастливые семьи"
END_MARK = "несомненный смысл добра"
OUT_DIR = Path("data")


def decode(raw):
    def score(text):
        low = text.lower()
        return low.count(" что ") + low.count(" не ") + low.count(" и ")

    candidates = [raw.decode(enc, errors="replace") for enc in ("utf-8", "cp1251", "koi8-r")]
    return max(candidates, key=score)


def load(source):
    if source:
        raw = Path(source).read_bytes()
    else:
        with urllib.request.urlopen(URL, timeout=60) as response:
            raw = response.read()
    return decode(raw)


def strip_html(text):
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def normalize(text):
    text = text.lower().replace("ё", "е")
    if MERGE_HARD_SIGN:
        text = text.replace("ъ", "ь")
    start, end = text.find(START_MARK), text.rfind(END_MARK)
    if start >= 0 and end > start:
        text = text[start:end + len(END_MARK)]
    else:
        print("Увага: межі роману не знайдено, використано весь текст. Приберіть службові рядки вручну.")
    text = re.sub(r"[^а-я ]", " ", text)
    return re.sub(r" +", " ", text).strip()


def main():
    source = next((a for a in sys.argv[1:] if a.lower().endswith((".html", ".htm", ".shtml", ".txt"))), None)
    text = normalize(strip_html(load(source)))
    no_spaces = text.replace(" ", "")

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "text_with_spaces.txt").write_text(text, encoding="utf-8")
    (OUT_DIR / "text_no_spaces.txt").write_text(no_spaces, encoding="utf-8")

    print(f"З пробілами: {len(text)} символів")
    print(f"Без пробілів: {len(no_spaces)} символів")
    print(f"Унікальних літер: {len(set(no_spaces))}")
    if len(no_spaces) < 1_000_000:
        print("Увага: без пробілів менше 1 млн символів, візьміть більший текст.")


if __name__ == "__main__":
    main()
