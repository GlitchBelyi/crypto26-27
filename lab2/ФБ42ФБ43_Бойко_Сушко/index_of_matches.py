from collections import Counter
import sys

if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()

    counter = Counter(text)

    _sum = 0
    
    for _, count in counter.most_common():
        _sum += (count) * (count - 1)

    index_of_matches = _sum / (len(text) * (len(text) - 1))

    print(f'Index of matches: {index_of_matches:.6f}')