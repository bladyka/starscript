import streamlit as st

# Расширенный словарь концептов
concepts = {
    "лодка": {"ключи": ["вода", "движение", "дерево"], "zs": "Selven"},
    "корабль": {"ключи": ["металл", "движение", "вода"], "zs": "Zortan"},
    "машина": {"ключи": ["движение", "металл", "объект"], "zs": "Tarnok"},
    "ракета": {"ключи": ["движение", "огонь", "воздух", "металл"], "zs": "Fyroven"},
    "любовь": {"ключи": ["привязанность", "чувство", "человек"], "zs": "Haleya"},
    "врач": {"ключи": ["человек", "знание", "исцеление"], "zs": "Medalyn"},
    "огонь": {"ключи": ["огонь"], "zs": "Fyra"},
    "вода": {"ключи": ["вода"], "zs": "Vel"},
    "дерево": {"ключи": ["дерево"], "zs": "Drak"},
    "движение": {"ключи": ["движение"], "zs": "Tra"},
    "объект": {"ключи": ["объект"], "zs": "Nol"},
    "металл": {"ключи": ["металл"], "zs": "Fer"},
    "воздух": {"ключи": ["воздух"], "zs": "Ael"},
    "дом": {"ключи": ["жилище", "приют", "дом"], "zs": "Homar"},
    "инструмент": {"ключи": ["инструмент", "объект", "использование"], "zs": "Toolen"},
    "воин": {"ключи": ["человек", "оружие", "сражение"], "zs": "Varak"},
    "оружие": {"ключи": ["оружие", "сражение"], "zs": "Blastr"},
    "друг": {"ключи": ["друг", "доверие", "привязанность"], "zs": "Aluron"},
    "еда": {"ключи": ["еда", "питание"], "zs": "Narka"},
    "время": {"ключи": ["время"], "zs": "Tymar"},
    "разум": {"ключи": ["мозг", "разум", "мысль"], "zs": "Intar"},
    "память": {"ключи": ["воспоминание", "прошлое", "мозг"], "zs": "Remno"},
    "язык": {"ключи": ["язык", "общение", "знание"], "zs": "Linguen"},
    "искусство": {"ключи": ["творчество", "выражение", "чувство"], "zs": "Arteon"},
    "свет": {"ключи": ["свет", "энергия"], "zs": "Luma"},
    "тьма": {"ключи": ["тьма", "отсутствие света"], "zs": "Nox"},
    "энергия": {"ключи": ["энергия", "движение"], "zs": "Ener"},
    "жизнь": {"ключи": ["жизнь", "организм", "движение"], "zs": "Vita"},
    "смерть": {"ключи": ["смерть", "остановка", "конец"], "zs": "Morto"},
}

# Обратный словарь для перевода с ZS
zs_to_human = {v["zs"].lower(): (k, ", ".join(v["ключи"])) for k, v in concepts.items()}

def find_best_match(word):
    # Простой словарь расширенных ассоциаций
    extended_map = {
        "любовь": ["чувство", "привязанность", "друг"],
        "ракета": ["металл", "движение", "огонь", "воздух"],
        "лодка": ["вода", "движение", "дерево"],
        "машина": ["движение", "металл", "объект"],
        "врач": ["человек", "знание", "исцеление"],
        "друг": ["доверие", "привязанность"],
        "память": ["прошлое", "мозг", "воспоминание"],
        "инструмент": ["объект", "использование"],
        "воин": ["оружие", "сражение", "человек"],
        "еда": ["питание"],
        "жизнь": ["организм", "движение"],
        "смерть": ["остановка", "конец"],
    }

    input_keys = extended_map.get(word, [word])

    # Подбор ближайшего концепта
    best_match = None
    max_overlap = 0

    for concept, data in concepts.items():
        overlap = len(set(input_keys) & set(data["ключи"]))
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = (concept, data["zs"], data["ключи"])

    if best_match:
        return best_match[1], best_match[0], ", ".join(best_match[2])
    else:
        return "—", "Не найдено", "Н/Д"

# Streamlit UI
st.set_page_config(page_title="Zvezdny Skript Translator", page_icon="🛸")
st.title("🛸 Zvezdny Skript Translator")
st.markdown("**Enter a human concept – get its alien equivalent.**")

tab1, tab2 = st.tabs(["➡️ Human → Alien", "⬅️ Alien → Human"])

with tab1:
    user_input = st.text_input("Enter a word (e.g. любовь, ракета, врач):")
    if user_input:
        zs_word, matched, details = find_best_match(user_input.lower())
        st.markdown(f"### 🧬 ZS Word: `{zs_word}`")
        st.markdown(f"**Matched Concept:** {matched}")
        st.markdown(f"**Meaning Components:** {details}")

with tab2:
    zs_input = st.text_input("Enter ZS word (e.g. Selven):")
    if zs_input:
        result = zs_to_human.get(zs_input.lower(), ("Unknown", "—"))
        st.markdown(f"### 🧠 Earth Concept: `{result[0]}`")
        st.markdown(f"**Keys:** {result[1]}")