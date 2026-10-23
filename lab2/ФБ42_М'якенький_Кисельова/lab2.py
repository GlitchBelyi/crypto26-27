from re import sub
from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
ALPHABET_LEN = len(ALPHABET)

def preprocess(filename):
    file = open(filename, "r", encoding="utf-8")
    text = file.read()
    text = text.lower()
    text = sub(r'[^а-я]', '', text)
    return text

def vizhener_encrypt(cleartext, key):
    r = len(key)
    ciphertext = ""
    i = 0
    for letter in cleartext:
        index = ALPHABET.find(letter)
        key_index = ALPHABET.index(key[i % r])
        cipher_index = (index + key_index) % ALPHABET_LEN
        ciphertext += ALPHABET[cipher_index]
        i = (i + 1) % r
    return ciphertext

def occurence_number(text, letter):
    count = 0
    for lett in text:
        if lett == letter:
            count += 1
    return count

def affinity_index(text):
    result = 0

    for letter in ALPHABET:
        nt = occurence_number(text, letter)
        result += nt * (nt - 1)
    n = len(text)
    return result / (n * (n - 1))

def find_r(text, theor_aff_i, error=0.01, max_r=30):
    candidates = []
    
    for r in range(2, max_r + 1):
        blocks = [affinity_index(text[i::r]) for i in range(r)]
        avg_aff_i = sum(blocks) / len(blocks)
        print(f'{r}: {avg_aff_i}')
        diff = abs(theor_aff_i - avg_aff_i)
        if diff <= error:
            candidates.append(r)
    print(f"Candidates: {candidates}")
    return candidates[0] if candidates else -1

def vizhener_decrypt(ciphertext, key):
    r = len(key)
    cleartext = ""

    for i, letter in enumerate(ciphertext):
        index = ALPHABET.index(letter)
        key_index = ALPHABET.index(key[i % r])
        clear_index = (index - key_index) % ALPHABET_LEN
        cleartext += ALPHABET[clear_index]

    return cleartext


def letter_frequencies(text):
    counts = Counter(text)
    n = len(text)

    return {
        letter: (counts[letter] + 1) / (n + ALPHABET_LEN)
        for letter in ALPHABET
    }


def chi_squared(text, frequencies):   
    counts = Counter(text)
    n = len(text)
    result = 0

    for letter in ALPHABET:
        observed = counts[letter]
        expected = n * frequencies[letter]
        result += (observed - expected) ** 2 / expected

    return result


def recover_key(ciphertext, r, frequencies):
    key = ""
    total_score = 0

    for i in range(r):
        block = ciphertext[i::r]
        candidates = []

        for letter in ALPHABET:
            decrypted = vizhener_decrypt(block, letter)
            score = chi_squared(decrypted, frequencies)
            candidates.append((score, letter))

        candidates.sort()

        best_score, best_letter = candidates[0]
        key += best_letter
        total_score += best_score

        print(f"\nKey position {i + 1}:")
        for score, letter in candidates[:5]:
            print(f"  {letter}: chi2 = {score:.4f}")

        print(f"Selected: {best_letter}")

    return key, total_score


def save_text(filename, text):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

def change_key(key, position=0):
    old_index = ALPHABET.index(key[position])
    new_letter = ALPHABET[(old_index + 1) % ALPHABET_LEN]

    return key[:position] + new_letter + key[position + 1:]



def main():
    
    # 1

    text = preprocess("./TEXT_UTF8")
    keys = [
        "от",
        "спа",
        "вухо",
        "сонце",
        "договоренность"
    ]
    theor_aff_i = affinity_index(text)
    print(f"For cleartext: {theor_aff_i}")
    for key in keys:
        ciphertext = vizhener_encrypt(text, key)
        print(f"For ciphertext (key: {key}): {affinity_index(ciphertext)}")
    # as expected, I(Y) becomes smaller as r becomes bigger

    # 2
    ciphertext = preprocess('./variant_10.txt')
    print(find_r(ciphertext, theor_aff_i))
    # Reasoning for this candidate:
    # Looking at the output of find_r, it's clear that the I(Y) is closest to the theoretical one when we are checking a multiple of r. 
    # This happens because blocks created by bigger multiples are subsets of the least multiple's block, although with less data.
    # Therefore the smallest multiple is the primary candidate
    # For other candidates the rest of the multiples in our range are picked

    # 3

    r = 15
    frequencies = letter_frequencies(text)

    print("\n=== KEY RECOVERY ===")
    key, score = recover_key(ciphertext, r, frequencies)

    print(f"\nRecovered key: {key}")
    print(f"Total chi2: {score:.4f}")

    decrypted = vizhener_decrypt(ciphertext, key)

    print("\nDecrypted text (first 500 characters):")
    print(decrypted[:500])

    save_text("decrypted.txt", decrypted)

    # 4

    print("\n=== KEY ERROR EXPERIMENT ===")

    print(f"Prediction: {100 / len(key):.2f}% of characters will change")

    wrong_key = change_key(key)
    wrong_decrypted = vizhener_decrypt(ciphertext, wrong_key)

    errors = sum(
        a != b for a, b in zip(decrypted, wrong_decrypted)
    )
    error_rate = errors / len(decrypted)

    print(f"Correct key: {key}")
    print(f"Modified key: {wrong_key}")
    print(f"Different characters: {errors}")
    print(f"Error percentage: {error_rate * 100:.2f}%")
    print(f"Theoretical percentage: {100 / len(key):.2f}%")

    print("\nDecrypted with incorrect key (first 500):")
    print(wrong_decrypted[:500])

    save_text("decrypted_wrong_key.txt", wrong_decrypted)
    

if __name__ == "__main__":
    main()
