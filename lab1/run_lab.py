import json
from collections import Counter
from entropy_lab import (
    RUSSIAN_ALPHABET, ALPHABET_WITH_SPACE,
    normalize_text, remove_spaces,
    symbol_frequencies, bigram_frequencies, top_n,
    h1, h2_per_symbol,
    make_sequence_B, make_sequence_V, make_sequence_G, make_sequence_D,
    redundancy,
)

CORPUS_PATH = "corpus.txt"

with open(CORPUS_PATH, encoding="utf-8") as f:
    raw = f.read()

text_with_spaces = normalize_text(raw, ALPHABET_WITH_SPACE)
text_no_spaces = remove_spaces(text_with_spaces)

results = {}
results["corpus_len_chars_raw"] = len(raw)
results["corpus_len_with_spaces"] = len(text_with_spaces)
results["corpus_len_no_spaces"] = len(text_no_spaces)

for label, text, alphabet in [
    ("with_spaces", text_with_spaces, ALPHABET_WITH_SPACE),
    ("no_spaces", text_no_spaces, RUSSIAN_ALPHABET),
]:
    section = {}
    freqs = symbol_frequencies(text)
    section["top5_symbols"] = top_n(freqs, 5)
    section["H1"] = h1(text)

    bg_over = bigram_frequencies(text, overlapping=True)
    bg_non = bigram_frequencies(text, overlapping=False)
    section["top5_bigrams_overlap"] = top_n(bg_over, 5)
    section["top5_bigrams_nonoverlap"] = top_n(bg_non, 5)
    section["H2_overlap"] = h2_per_symbol(text, overlapping=True)
    section["H2_nonoverlap"] = h2_per_symbol(text, overlapping=False)
    section["alphabet_size"] = len(alphabet)
    results[label] = section

# послідовності А, Б, В
seq_len = min(20000, len(text_no_spaces))
A = text_no_spaces[:seq_len]
B = make_sequence_B("о", seq_len)
V = make_sequence_V(RUSSIAN_ALPHABET, seq_len)

results["section3"] = {
    "length": seq_len,
    "H1_A": h1(A),
    "H1_B": h1(B),
    "H1_V": h1(V),
}

# Розділ 5 звіту: послідовності Г, Д
gd_len = min(20000, len(text_no_spaces))
G = make_sequence_G(text_no_spaces, gd_len)
top2 = [s for s, _ in Counter(text_no_spaces).most_common(2)]
D = make_sequence_D(top2, gd_len)

results["section4"] = {
    "length": gd_len,
    "H1_G": h1(G),
    "H1_D": h1(D),
    "H2_overlap_G": h2_per_symbol(G, overlapping=True),
    "H2_nonoverlap_G": h2_per_symbol(G, overlapping=False),
    "H2_overlap_D": h2_per_symbol(D, overlapping=True),
    "H2_nonoverlap_D": h2_per_symbol(D, overlapping=False),
}

# Розділ 7 звіту: надлишковість (H1, H2)
m_no_space = len(RUSSIAN_ALPHABET)
results["section6"] = {
    "R_H1_no_space": redundancy(results["no_spaces"]["H1"], m_no_space),
    "R_H2_no_space": redundancy(results["no_spaces"]["H2_overlap"], m_no_space),
}

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(json.dumps(results, ensure_ascii=False, indent=2))
