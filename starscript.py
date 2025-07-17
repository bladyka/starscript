import streamlit as st
import hashlib
import json
import os
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

DICT_PATH = "alien_dict.json"

# Загружаем или создаём словарь
if os.path.exists(DICT_PATH):
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        alien_dict = json.load(f)
else:
    alien_dict = {}

lemmatizer = WordNetLemmatizer()

SYLLABLES = [
    "ka", "lo", "mi", "re", "zu", "na", "shi", "to", "va",
    "xi", "pa", "ru", "se", "di", "ne"
]

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
    "star": "suur",
    "you": "va-lo",
    "your": "va-lo"
}

def to_lemma(word):
    return lemmatizer.lemmatize(word.lower())

def generate_alien_word(lemma):
    if lemma in BASE_ROOTS:
        return BASE_ROOTS[lemma]
    # Генерируем слово из 3 слогов по md5 хешу
    h = hashlib.md5(lemma.encode()).hexdigest()
    sylls = []
    for i in range(0, 6, 2):
        val = int(h[i:i+2], 16)
        sylls.append(SYLLABLES[val % len(SYLLABLES)])
    return "-".join(sylls)

def translate_word(word):
    w = word.lower()
    if w in alien_dict:
        return alien_dict[w], "From cache"
    lemma = to_lemma(w)
    alien_word = generate_alien_word(lemma)
    alien_dict[w] = alien_word
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(alien_dict, f, ensure_ascii=False, indent=2)
    return alien_word, "Generated"

def translate_phrase(phrase):
    words = phrase.strip().split()
    translated_parts = [translate_word(w)[0] for w in words]
    # Объединяем части в одно слово без дефисов, чтобы звучало как единое слово
    return "".join(translated_parts)

st.title("🚀 Zvezdniy Skript Translator")

text = st.text_input("Enter any English word or phrase:")

if text:
    translation = translate_phrase(text)
    st.subheader("Translation:")
    st.write(translation)
