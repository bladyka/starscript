import streamlit as st
import json
import os
import re
import nltk
from nltk.corpus import wordnet as wn
from sentence_transformers import SentenceTransformer, util

# ========== Загрузка NLTK ==========
nltk.download('wordnet')
nltk.download('omw-1.4')

# ========== Пути ==========
DICT_PATH = "dynamic_dict.json"

# ========== Загрузка или создание словаря ==========
if os.path.exists(DICT_PATH):
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        dynamic_dict = json.load(f)
else:
    dynamic_dict = {}

# ========== Базовый словарь Звёздного Скрипта ==========
base_concept_dict = {
    "person": "Haleya",
    "human": "Haleya",
    "emotion": "Nira",
    "knowledge": "Etha",
    "death": "Mor",
    "life": "Zura",
    "machine": "Karn",
    "generator": "Karn",
    "device": "Karn",
    "movement": "Teyu",
    "motion": "Teyu",
    "travel": "Teyu",
    "water": "Sel",
    "fire": "Fyrn",
    "air": "Aen",
    "earth": "Terra",
    "wood": "Darn",
    "object": "Hal",
    "structure": "Varn",
    "building": "Varn",
    "light": "Luma",
    "dark": "Nokta",
    "small": "Min",
    "big": "Maxa",
    "sound": "Sonar",
    "color": "Tinta",
    "energy": "Vorr",
    "power": "Vorr",
    "weapon": "Klyth",
    "war": "Drav",
    "love": "Niraleya",
    "fear": "Noknira",
    "animal": "Bestan",
    "food": "Kora",
    "plant": "Flor",
    "metal": "Ferr",
    "stone": "Roka",
    "sky": "Zenn",
    "child": "Halet",
    "language": "Lekth",
    "communication": "Lekth",
    "technology": "Karth",
    "time": "Temar",
    "future": "Temarix",
    "past": "Temara",
    "space": "Vex",
    "universe": "Omn",
    "data": "Koda",
    "memory": "Memn",
    "tool": "Instr",
    "shield": "Proteka"
}

# ========== Модель ==========
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# ========== Функции ==========

def save_dict():
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(dynamic_dict, f, ensure_ascii=False, indent=2)

def split_compound(word):
    parts = re.findall('[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', word)
    return [p.lower() for p in parts] if parts else [word.lower()]

def get_concepts(word):
    synsets = wn.synsets(word)
    if not synsets:
        return []
    concepts = set()
    for syn in synsets:
        # Гипернимы (родовые понятия)
        for hyper in syn.hypernyms():
            lemma = hyper.lemmas()[0].name().lower()
            if lemma in base_concept_dict:
                concepts.add(lemma)
        # Леммы самого слова
        for lemma in syn.lemmas():
            l = lemma.name().lower()
            if l in base_concept_dict:
                concepts.add(l)
    return list(concepts)

def generate_translation(word):
    # Разбиваем на части
    parts = split_compound(word)
    found_concepts = set()
    for part in parts:
        concepts = get_concepts(part)
        if concepts:
            found_concepts.update(concepts)
    if found_concepts:
        # Собираем перевод из базовых концептов
        return "-".join(sorted(base_concept_dict[c] for c in found_concepts))
    else:
        # Если нет концептов — просто возвращаем слово с пометкой
        return f"[Unknown: {word}]"

def translate(word):
    word_lower = word.lower()
    if word_lower in dynamic_dict:
        return dynamic_dict[word_lower]
    else:
        translation = generate_translation(word_lower)
        dynamic_dict[word_lower] = translation
        save_dict()
        return translation

# ========== Streamlit UI ==========

st.title("Dynamic Zvezdny Script Translator 🛸")
st.write("Type any English word or phrase. New words get logically analyzed and added to the dictionary automatically!")

user_input = st.text_input("Enter English word or phrase:")

if user_input:
    # Разбиваем фразу на слова
    words = re.findall(r'\w+', user_input)
    translations = []
    for w in words:
        translations.append(translate(w))
    st.markdown("### Translation:")
    st.write(" • ".join(translations))
