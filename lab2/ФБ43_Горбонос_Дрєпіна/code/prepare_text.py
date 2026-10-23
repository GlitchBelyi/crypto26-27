import sys
from vigenere import DATA, prepare

with open(sys.argv[1], encoding="utf-8") as f:
    text = prepare(f.read())
n = int(sys.argv[2]) if len(sys.argv) > 2 else 2800
(DATA / "plaintext.txt").write_text(text[:n], encoding="utf-8")
print(f"Збережено data/plaintext.txt: {len(text[:n])} літер із {len(text)}")
