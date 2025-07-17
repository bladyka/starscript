import streamlit as st
import hashlib
import json
import os

DICT_PATH = "alien_dict.json"

# Загрузка или создание словаря
if os.path.exists(DICT_PATH):
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        alien_dict = json.load(f)
else:
    alien_dict = {}

def generate_alien_word(english_word):
    h = hashlib.md5(english_word.encode()).hexdigest()[:6]
    syllables = [h[i:i+2] for i in range(0, len(h), 2)]
    alien_syllables = []
    for s in syllables:
        chars = []
        for c in s:
            val = int(c, 16)
            chars.append(chr(ord('a') + val))
        alien_syllables.append("".join(chars))
    return "-".join(alien_syllables)

def translate(word):
    w = word.lower()
    if w in alien_dict:
        return alien_dict[w], "From dictionary"
    alien_word = generate_alien_word(w)
    alien_dict[w] = alien_word
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(alien_dict, f, ensure_ascii=False, indent=2)
    return alien_word, "Generated new"

st.title("🚀 Zvezdniy Skript Universal Translator")

text = st.text_input("Enter any English word or phrase:")

if text:
    words = text.strip().split()
    results = []
    explanations = []
    for w in words:
        tr, expl = translate(w)
        results.append(tr)
        explanations.append(f"**{w}** → {tr} ({expl})")
    st.subheader("Translation:")
    st.write(" ".join(results))
    st.subheader("Details:")
    st.markdown("\n\n".join(explanations))
