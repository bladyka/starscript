import streamlit as st

# Модульная база понятий
concepts = {
    "лодка": {"ключи": ["вода", "движение", "дерево"], "zs": "Selven"},
    "корабль": {"ключи": ["вода", "движение", "металл"], "zs": "Zortan"},
    "огонь": {"ключи": ["огонь"], "zs": "Fyra"},
    "дерево": {"ключи": ["дерево"], "zs": "Drak"},
    "вода": {"ключи": ["вода"], "zs": "Vel"},
    "движение": {"ключи": ["движение"], "zs": "Tra"},
    "объект": {"ключи": ["объект"], "zs": "Nol"},
    "металл": {"ключи": ["металл"], "zs": "Fer"},
    "воздух": {"ключи": ["воздух"], "zs": "Ael"},
    "дом": {"ключи": ["дом", "приют", "жилище"], "zs": "Homar"},
}

def translate_to_zs(input_text):
    words = input_text.lower().split()
    matches = []

    for word in words:
        for concept, data in concepts.items():
            if word in data["ключи"]:
                matches.append(concept)
                break

    # Поиск составного понятия
    for target, data in concepts.items():
        if set(data["ключи"]).issubset(set(words)):
            return data["zs"], target

    # Иначе по частям
    zs_words = []
    for concept in matches:
        zs_word = concepts[concept]["zs"]
        if zs_word not in zs_words:
            zs_words.append(zs_word)

    return "-".join(zs_words), " + ".join(matches)

def translate_to_human(zs_input):
    for concept, data in concepts.items():
        if zs_input.lower() == data["zs"].lower():
            return concept, ", ".join(data["ключи"])
    return "Неизвестно", "—"

# Streamlit UI
st.set_page_config(page_title="Zvezdny Skript Translator", page_icon="🛸")

st.title("🛸 Zvezdny Skript Translator")

st.markdown("**Enter Earth-language words to get their alien equivalent.**")

tab1, tab2 = st.tabs(["➡️ Translate to ZS", "⬅️ Translate to Human"])

with tab1:
    user_input = st.text_input("Enter words (e.g. вода движение дерево):")
    if user_input:
        alien_word, explanation = translate_to_zs(user_input)
        st.markdown(f"### 🧬 Result: `{alien_word}`")
        st.markdown(f"**Meaning:** {explanation}")

with tab2:
    zs_input = st.text_input("Enter ZS word (e.g. Selven):")
    if zs_input:
        earth_word, keywords = translate_to_human(zs_input)
        st.markdown(f"### 🧠 Earth Meaning: `{earth_word}`")
        st.markdown(f"**Context:** {keywords}")