from re import sub
from math import log
from itertools import islice
from random import choice

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '

def preprocess(filename):
    file = open(filename, "r")
    text = file.read()
    text = text.lower()
    text = sub(r'[^а-яё\s]', '', text) # only russian
    text = sub(r'\s+', ' ', text) # only spaces
    text_nospaces = sub(r' ', '', text)
    return (text, text_nospaces)

def prob_dist_1(text):
    dist = {}
    for symbol in text:
        dist[symbol] = dist.get(symbol, 0) + 1
    for k in dist:
        dist[k] /= len(text)
    return dist

def prob_dist_2(text):
    dist = {}
    count = 0
    for i in range(0, len(text)-1):
        bigram = text[i:i+2]
        dist[bigram] = dist.get(bigram, 0) + 1
        count += 1
    for k in dist:
        dist[k] /= count
    return dist

def prob_dist_2_no_intersect(text):
    dist = {}
    count = 0
    for i in range(0, len(text)-1, 2):
        bigram = text[i:i+2]
        dist[bigram] = dist.get(bigram, 0) + 1
        count += 1
    for k in dist:
        dist[k] /= count
    return dist

def H_1(dist):
    sum = 0
    for i in dist:
        sum += dist[i] * log(dist[i], 2)
    return sum * -1

def H_2(dist):
    sum = 0
    for i in dist:
        sum += dist[i] * log(dist[i], 2)
    return sum * -0.5

def dist_max_n(dist, n):
    sorted_dict = dict(sorted(dist.items(), key=lambda item: item[1], reverse=True))
    return dict(islice(sorted_dict.items(), n))

def main():
    text, text_nospaces = preprocess("TEXT_UTF8")

    # 2

    print("For text with spaces")

    print("Symbols")
    dist = prob_dist_1(text)
    print(f"Most common: {dist_max_n(dist, 5)}")
    print(f"H_1: {H_1(dist)}")

    print("Bigrams")
    dist = prob_dist_2(text)
    print(f"Most common: {dist_max_n(dist, 5)}")
    print(f"H_2: {H_2(dist)}")

    print("Bigrams (no intersection)")
    dist = prob_dist_2_no_intersect(text)
    print(f"Most common: {dist_max_n(dist, 5)}")
    print(f"H_2: {H_2(dist)}")

    print("For text without spaces")

    print("Symbols")
    dist = prob_dist_1(text_nospaces)
    print(f"Most common: {dist_max_n(dist, 5)}")
    print(f"H_1: {H_1(dist)}")

    print("Bigrams")
    dist = prob_dist_2(text_nospaces)
    print(f"Most common: {dist_max_n(dist, 5)}")
    print(f"H_2: {H_2(dist)}")

    print("Bigrams (no intersection)")
    dist = prob_dist_2_no_intersect(text_nospaces)
    print(f"Most common: {dist_max_n(dist, 5)}")
    print(f"H_2: {H_2(dist)}")

    # 3

    text_len = len(text)
    seq_a = text
    seq_b = "a" * text_len
    seq_c = ""
    for i in range(text_len):
        seq_c += choice(list(ALPHABET))
    
    #prediction: H(B) < H(A) < H(C)
    dist = prob_dist_1(seq_a)
    print(f"for A: {H_1(dist)}")
    dist = prob_dist_1(seq_b)
    print(f"for B: {H_1(dist)}")
    dist = prob_dist_1(seq_c)
    print(f"for C: {H_1(dist)}")

    # 4

    N = 1000 
    alphabet = ["а", "б"]

    seq_D = ""
    for i in range(N):
        seq_D += alphabet[i % 2] 

    from random import shuffle
    seq_G_list = list(seq_D)
    shuffle(seq_G_list)
    seq_G = "".join(seq_G_list)

    print("Sequence D (periodic)")
    print("H1(D) =", H_1(prob_dist_1(seq_D)))
    print("H2(D, intersect) =", H_2(prob_dist_2(seq_D)))
    print("H2(D, non-intersect) =", H_2(prob_dist_2_no_intersect(seq_D)))

    print("Sequence G (random)")
    print("H1(G) =", H_1(prob_dist_1(seq_G)))
    print("H2(G, intersect) =", H_2(prob_dist_2(seq_G)))
    print("H2(G, non-intersect) =", H_2(prob_dist_2_no_intersect(seq_G)))

if __name__ == "__main__":
    main()
