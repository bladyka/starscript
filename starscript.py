import streamlit as st
import hashlib
import json
import os
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

DICT_PATH = "alien_dict.json"

if os.path.exists(DICT_PATH):
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        alien_dict = json.load(f)
else:
    alien_dict = {}

lemmatizer = WordNetLemmatizer()

SYLLABLES = [
    "ka", "lo", "mi", "re", "zu", "na", "shi", "to", "va", "xi", "pa", "ru", "se", "di", "ne"
]

# Базовые корни (лексикон)
BASE_ROOTS = {
    "water": "sel",
    "fire": "ver",
    "earth": "tur",
    "wind": "kai",
    "movement": "nol",
    "light": "phi",
    "darkness": "zor",
    "object": "kal",
    "life": "hal",
    "death": "mir",
    "tree": "lor",
    "metal": "zek",
    "sky": "tha",
    "sound": "rak",
    "energy": "ven",
    "emotion": "lii",
    "structure": "bal",
    "technology": "syn",
    "knowledge": "mek",
    "heat": "zor",
    "space": "qel",
    "body": "kor",
    "limb": "dra",
    "mother": "hala",
    "sun": "suur",
    "engine": "syn-nol-ven",
    "leg": "kor-dra",
    "human": "haleya",
    "love": "lii-hal",
    "boat": "kal-nol-sel-lor",
    "star": "suur"
}

def word_to_lemma(word):
    return lemmatizer.lemmatize(word.lower())

def generate_alien_word(english_word):
    lemma = word_to_lemma(english_word)
    # Если есть в базовых корнях — возвращаем их напрямую
    if lemma in BASE_ROOTS:
        return BASE_ROOTS[lemma]
    # Иначе генерируем по хешу
    h = hashlib.md5(lemma.encode()).hexdigest()
    parts = [h[i:i+2] for i in range(0, 6, 2)]
    syllables = []
    for p in parts:
        val = int(p, 16)
        syllable = SYLLABLES[val % len(SYLLABLES)]
        syllables.append(syllable)
    return "-".join(syllables)

def translate(word):
    w = word.lower()
    if w in alien_dict:
        return alien_dict[w], "From dictionary"
    alien_word = generate_alien_word(w)
    alien_dict[w] = alien_word
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(alien_dict, f, ensure_ascii=False, indent=2)
    return alien_word, "Generated new"

# Позволяет строить составные слова из нескольких
def translate_phrase(phrase):
    words = phrase.strip().split()
    parts = []
    for w in words:
        tr, _ = translate(w)
        parts.append(tr)
    return "-".join(parts)

st.title("🚀 Zvezdniy Skript Universal Translator")

text = st.text_input("Enter any English word or phrase:")

if text:
    translation = translate_phrase(text)
    st.subheader("Translation:")
    st.write(translation)
