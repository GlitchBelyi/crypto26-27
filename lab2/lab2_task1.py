"""Завдання 1. індекси відповідності відкритого тексту та шифртекстів"""
import json
from vigenere import *
 
plain = load("plain_text.txt")
keys = ["да", "мир", "луна", "книга", "криптоаналитик"]
 
rows = [("відкритий текст", "—", 1, index_of_coincidence(plain))]
for k in keys:
    rows.append(("шифртекст", k, len(k), index_of_coincidence(encrypt(plain, k))))
 
print(f"n = {len(plain)}, I теор. = {I_THEORY:.5f}, 1/m = {I_RANDOM:.5f}")
print(f"{'текст':<16}{'ключ':<16}{'r':<4}{'I':<8}")
for name, k, r, ic in rows:
    print(f"{name:<16}{k:<16}{r:<4}{ic:.5f}")
 
json.dump({"n": len(plain), "I_theory": I_THEORY, "I_random": I_RANDOM,
           "rows": rows}, open("task1.json", "w", encoding="utf-8"), ensure_ascii=False)