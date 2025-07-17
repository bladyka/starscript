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

# Набор слогов для генерации слов (удобочитаемые)
SYLLABLES = [
    "ka", "lo", "mi", "re", "zu", "na", "shi", "to", "va",
    "xi", "pa", "ru", "se", "di", "ne"
]

# База корней и производных: корень -> инопланетский корень
ROOTS = {
    "water": "sel",
    "fire": "ver",
    "earth": "tur",
    "wind": "kai",
    "move": "nol",
    "light": "phi",
    "dark": "zor",
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
    "tech": "syn",
    "know": "mek",
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
    "your": "va-lo",
    # Добавим производные для теста
    "running": "nol",  # от move
    "run": "nol",
    "walk": "nol",
    "walked": "nol"
}

# Функция для поиска корней в слове (ищем максимально длинный корень)
def find_roots(word):
    word = word.lower()
    roots_found = []
    # Попытка найти корни, начиная с длинных
    sorted_roots = sorted(ROOTS.keys(), key=lambda x: -len(x))
    pos = 0
    while pos < len(word):
        matched = False
        for root in sorted_roots:
            if word.startswith(root, pos):
                roots_found.append(ROOTS[root])
                pos += len(root)
                matched = True
                break
        if not matched:
            # Если корень не нашли — добавляем один символ как заглушку
            roots_found.append(word[pos])
            pos += 1
    return roots_found

def generate_alien_word(word):
    # Для читаемости: из хеша делаем набор слогов
    h = hashlib.md5(word.encode()).hexdigest()
    sylls = []
    for i in range(0, 6, 2):
        val = int(h[i:i+2], 16)
        sylls.append(SYLLABLES[val % len(SYLLABLES)])
    return "-".join(sylls)

def to_lemma(word):
    return lemmatizer.lemmatize(word.lower())

def translate_word(word):
    w = word.lower()
    if w in alien_dict:
        return alien_dict[w], "From cache"
    lemma = to_lemma(w)
    roots = find_roots(lemma)
    # Если нашли хоть один корень из словаря, соединяем их
    if any(r in ROOTS.values() for r in roots):
        alien_word = "-".join(roots)
    else:
        alien_word = generate_alien_word(lemma)
    alien_dict[w] = alien_word
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(alien_dict, f, ensure_ascii=False, indent=2)
    return alien_word, "Translated"

def translate_phrase(phrase):
    words = phrase.strip().split()
    translated_parts = [translate_word(w)[0] for w in words]
    return "-".join(translated_parts)

st.title("🚀 Zvezdniy Skript Improved Translator")

text = st.text_input("Enter any English word or phrase:")

if text:
    translation = translate_phrase(text)
    st.subheader("Translation:")
    st.write(translation)
