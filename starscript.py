import streamlit as st
from sentence_transformers import SentenceTransformer, util
import json
import os
import hashlib

# Загрузка модели для семантического поиска
model = SentenceTransformer('all-MiniLM-L6-v2')

BASE_CONCEPTS = {
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

# Кэш переводов
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

# Подготавливаем базу для поиска
base_phrases = list(BASE_CONCEPTS.keys())
base_embeddings = model.encode(base_phrases, convert_to_tensor=True)

def semantic_translate(word):
    word_lower = word.lower()
    if word_lower in dynamic_dict:
        return dynamic_dict[word_lower], "Cached translation"

    # Семантический поиск по базе концептов
    query_emb = model.encode(word_lower, convert_to_tensor=True)
    hits = util.semantic_search(query_emb, base_embeddings, top_k=3)[0]

    # Собираем перевод из лучших совпадений, если они достаточно близки
    threshold = 0.5
    parts = []
    explanation = []
    for hit in hits:
        if hit['score'] >= threshold:
            concept = base_phrases[hit['corpus_id']]
            parts.append(BASE_CONCEPTS[concept])
            explanation.append(f"{concept} ({hit['score']:.2f})")

    if not parts:
        # Если нет похожих — создаём хеш и ставим знак вопроса
        hash_key = hashlib.md5(word_lower.encode()).hexdigest()[:4]
        alien_word = f"???-{hash_key}"
        dynamic_dict[word_lower] = alien_word
        save_dynamic_dict(dynamic_dict)
        return alien_word, "No similar concepts found"

    # Собираем перевод и сохраняем
    alien_word = "-".join(sorted(set(parts)))
    dynamic_dict[word_lower] = alien_word
    save_dynamic_dict(dynamic_dict)
    return alien_word, " + ".join(explanation)

# Streamlit UI
st.title("🌌 Zvezdniy Skript Ultimate Translator")
input_text = st.text_input("Enter any English word or phrase:")

if input_text:
    words = input_text.strip().split()
    translations = []
    explanations = []
    for w in words:
        tr, expl = semantic_translate(w)
        translations.append(tr)
        explanations.append(f"**{w}** → {tr} ({expl})")

    st.subheader("Translation:")
    st.write(" ".join(translations))

    st.subheader("Explanation:")
    st.markdown("\n\n".join(explanations))
