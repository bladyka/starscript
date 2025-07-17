import streamlit as st
import nltk
from nltk.corpus import wordnet as wn
import re

# Обязательно один раз скачать базы
nltk.download('wordnet')
nltk.download('omw-1.4')

# Словарь Звёздного Скрипта
concept_dict = {
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

def split_compound(word):
    # разбиваем camelCase и подобные на части
    parts = re.findall('[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', word)
    return [p.lower() for p in parts] if parts else [word.lower()]

def get_concepts(word):
    synsets = wn.synsets(word)
    if not synsets:
        return []
    concepts = set()
    for syn in synsets:
        # собираем родовые понятия (hypernyms)
        for hyper in syn.hypernyms():
            lemma = hyper.lemmas()[0].name().lower()
            if lemma in concept_dict:
                concepts.add(lemma)
        # также добавим саму лемму, если есть
        for lemma in syn.lemmas():
            l = lemma.name().lower()
            if l in concept_dict:
                concepts.add(l)
    return list(concepts)

def translate(text):
    words = re.findall(r'\w+', text.lower())
    final_concepts = set()

    for word in words:
        parts = split_compound(word)
        for part in parts:
            concepts = get_concepts(part)
            if concepts:
                final_concepts.update(concepts)

    if not final_concepts:
        return "Unknown"

    # Собираем перевод из концептов, сортируем для стабильности
    return "-".join(sorted(concept_dict[c] for c in final_concepts))

# Streamlit UI
st.title("Star Script Translator 🌌")
st.write("Enter English words, phrases or compound words, get Zvezdnyy Skript translation.")

input_text = st.text_input("Input:")

if input_text:
    translation = translate(input_text)
    st.markdown(f"**Translation:** `{translation}`")