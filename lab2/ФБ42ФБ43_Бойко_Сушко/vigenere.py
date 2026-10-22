import sys

def encrypt(text, key):
    result = []
    key_index = 0
    for char in text:
        shift = ord(key[key_index]) - ord('а')
        new_char = chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
        result.append(new_char)
        key_index = (key_index + 1) % len(key)

    return ''.join(result)

def decrypt(cyphered_text, key):
    result = []
    key_index = 0
    for char in cyphered_text:
        shift = ord(key[key_index]) - ord('а')
        new_char = chr((ord(char) - ord('а') - shift) % 32 + ord('а'))
        result.append(new_char)
        key_index = (key_index + 1) % len(key)

    return ''.join(result)

if __name__ == "__main__":
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()
    if sys.argv[4] == "d":
        cyphered_text = decrypt(text, sys.argv[2])
    elif sys.argv[4] == "e":
        cyphered_text = encrypt(text, sys.argv[2])

    with open(sys.argv[3], "w", encoding="utf-8") as f:
        f.write(cyphered_text)