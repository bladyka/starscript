import streamlit as st
import json
import os
import re
from sentence_transformers import SentenceTransformer, util

# --- Пути ---
DICT_PATH = "dynamic_dict.json"
WORDLIST_PATH = "english_words.txt"  # загрузи сам файл с https://github.com/dwyl/english-words/blob/master/words.txt

# --- Загрузка большого списка английских слов ---
@st.cache_data(show_spinner=False)
def load_wordlist():
    if os.path.exists(WORDLIST_PATH):
        with open(WORDLIST_PATH, "r", encoding="utf-8") as f:
            return set(w.strip().lower() for w in f if w.strip())
    else:
        st.warning(f"Wordlist file {WORDLIST_PATH} not found. Please download it and place in the app folder.")
        return set()

english_words = load_wordlist()

# --- Загрузка или создание динамического словаря ---
if os.path.exists(DICT_PATH):
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        dynamic_dict = json.load(f)
else:
    dynamic_dict = {}

# --- Базовый словарь концептов Звёздного Скрипта ---
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

# --- Загрузка модели ---
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# --- Функции ---
def save_dict():
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(dynamic_dict, f, ensure_ascii=False, indent=2)

def find_closest_concept(word):
    concepts = list(base_concept_dict.keys())
    concept_embs = model.encode(concepts, convert_to_tensor=True)
    word_emb = model.encode(word, convert_to_tensor=True)
    hits = util.semantic_search(word_emb, concept_embs, top_k=1)[0]
    if hits:
        best_concept = concepts[hits[0]['corpus_id']]
        return best_concept
    return None

def generate_translation(word):
    # Проверяем наличие слова в базе английских слов
    if word not in english_words:
        return f"[Unknown word: {word}]"
    # Пытаемся найти самый близкий концепт
    concept = find_closest_concept(word)
    if concept:
        return base_concept_dict[concept]
    else:
        return f"[No concept for: {word}]"

def translate(word):
    word_lower = word.lower()
    if word_lower in dynamic_dict:
        return dynamic_dict[word_lower]
    else:
        translation = generate_translation(word_lower)
        dynamic_dict[word_lower] = translation
        save_dict()
        return translation

# --- Streamlit UI ---
st.title("Universal Zvezdny Script Translator with Big English Wordlist 🚀")
st.write("Enter any English word. The app knows tons of words and translates logically to Zvezdny Script!")

user_input = st.text_input("Enter English word or phrase:")

if user_input:
    words = re.findall(r'\w+', user_input)
    translations = [translate(w) for w in words]
    st.markdown("### Translation:")
    st.write(" • ".join(translations))
