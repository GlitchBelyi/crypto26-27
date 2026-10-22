from collections import Counter
import sys

def calculate_of_key(text_block, r):
    n = len(text_block)
    if n <= 1:
        return None
        
    counter = Counter(text_block)
    
    counter_most_common = counter.most_common(3)

    if counter_most_common:
        for letter, _ in counter_most_common:
            key = chr((ord(letter) - ord('о')) % 32 + ord('а'))
            print(f"Ймовірна літера №{r} ключа: {key}")
        print()
        key_letter = chr((ord(counter_most_common[0][0]) - ord('о')) % 32 + ord('а'))
        return key_letter

if __name__ == '__main__':

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()

    r = int(sys.argv[2])

    possible_key = ''

    for j in range(r):
        block = text[j::r] 
        key_letter = calculate_of_key(block, j + 1)
        if key_letter:
            possible_key += key_letter

    print(f'Потенційний ключ: {possible_key}')