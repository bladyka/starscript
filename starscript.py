import streamlit as st
import nltk
from nltk.corpus import wordnet as wn
import json
import os
import hashlib
from starscript_dict import BASE_CONCEPTS

nltk.download('wordnet')
nltk.download('omw-1.4')

DYNAMIC_DICT_PATH = "dynamic_dict.json"

def load_dynamic_dict():
    if os.path.exists(DYNAMIC_DICT_PATH):
        with open(DYNAMIC_DICT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_dynamic_dict(d):
    with open(DYNAMIC_DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

dynamic_dict = load_dynamic_dict()

def split_word(word):
    parts = []
    # Разбиваем слово на части от длины 3 символов и больше
    for i in range(3, len(word)):
        left = word[:i]
        right = word[i:]
        if wn.synsets(left):
            parts.append(left)
        if wn.synsets(right):
            parts.append(right)
    return list(set(parts)) if parts else [word]

def get_concepts_from_definition(defn):
    defn = defn.lower()
    found = []
    for key, val in BASE_CONCEPTS.items():
        if key in defn:
            found.append(val)
    return found

def translate_word(word):
    word_lower = word.lower()
    if word_lower in dynamic_dict:
        return dynamic_dict[word_lower], "From dynamic dict"
    if word_lower in BASE_CONCEPTS:
        return BASE_CONCEPTS[word_lower], "From base concepts"
    synsets = wn.synsets(word_lower)
    if not synsets:
        # Если нет значения в WordNet, пытаемся разбить
        parts = split_word(word_lower)
        concepts = []
        for part in parts:
            syns = wn.synsets(part)
            if syns:
                defn = syns[0].definition()
                concepts.extend(get_concepts_from_definition(defn))
        concepts = list(set(concepts))
        if concepts:
            translation = "-".join(sorted(concepts))
            key_hash = hashlib.md5(word_lower.encode()).hexdigest()[:4]
            alien_word = f"{translation}-{key_hash}"
            dynamic_dict[word_lower] = alien_word
            save_dynamic_dict(dynamic_dict)
            return alien_word, f"Inferred from parts {parts}"
        else:
            dynamic_dict[word_lower] = "???"
            save_dynamic_dict(dynamic_dict)
            return "???", "No concept found"
    else:
        defn = synsets[0].definition()
        concepts = get_concepts_from_definition(defn)
        if concepts:
            translation = "-".join(sorted(set(concepts)))
            key_hash = hashlib.md5(word_lower.encode()).hexdigest()[:4]
            alien_word = f"{translation}-{key_hash}"
            dynamic_dict[word_lower] = alien_word
            save_dynamic_dict(dynamic_dict)
            return alien_word, f"From WordNet definition: {defn}"
        else:
            dynamic_dict[word_lower] = "???"
            save_dynamic_dict(dynamic_dict)
            return "???", "No concept matched"

st.title("🌌 Звёздный Скрипт — Универсальный Переводчик")

user_input = st.text_input("Введите любое английское слово или фразу:")

if user_input:
    words = user_input.strip().split()
    translations = []
    explanations = []
    for w in words:
        tr, expl = translate_word(w)
        translations.append(tr)
        explanations.append(f"**{w}** → {tr} ({expl})")
    st.subheader("Перевод:")
    st.write(" ".join(translations))
    st.subheader("Логика перевода:")
    for e in explanations:
        st.markdown(e)
