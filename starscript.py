import streamlit as st
from itertools import permutations

st.set_page_config(page_title="Star Script Translator", layout="centered")
st.title("⭐ Star Script Translator")

# Морфемы (атомы)
morphs = {
    'ven':'object','lun':'move','sel':'water','tik':'place',
    'ral':'light','mel':'mind','lam':'see','rak':'create',
    'sil':'destroy','nav':'ship','sul':'knowledge','zen':'understand',
    'kar':'many','tor':'direction','sen':'form','sim':'simple',
    'tan':'earth','lir':'air','sol':'fire','nul':'void',
    'val':'speak','nem':'feel','ser':'be','ke':'question',
    'ne':'negation','za':'possession','ta':'past','na':'future',
    'in':'inside','ex':'outside'
}

# Составные слова
composed = {
    'nav': ['ven','lun','sel','tik'],
    'sulmel': ['sul','mel'],
    'tormel': ['tor','mel'],
    'selven': ['sel','ven'],
    'lunsel': ['lun','sel'],
    'sulnav': ['sul','nav'],        # «интеллект-корабль»
    'nemmel': ['nem','mel'],        # сознательное чувство
    'zarlun': ['ral','lun'],        # светящийся движение
    'karven': ['kar','ven'],        # множество объектов
}

# Разбиение на морфемы
def breakdown(word):
    parts, buf, i = [], '', 0
    while i < len(word):
        buf += word[i]
        if buf in morphs:
            parts.append(buf)
            buf = ''
        i += 1
    if buf:
        parts.append(buf)
    return parts

def translate_forward(phrase):
    out = []
    for w in phrase.split():
        parts = breakdown(w)
        translation = ' + '.join(f"{p} ({morphs.get(p,'?')})" for p in parts)
        context = ''
        if w in composed:
            atoms = composed[w]
            words = ', '.join(f"{p}={morphs[p]}" for p in atoms)
            context = f" — full meaning: {words}"
        out.append(f"**{w}** → {translation}{context}")
    return out

def translate_reverse(atoms_input):
    tokens = atoms_input.strip().split()
    matches = []
    for word, atoms in composed.items():
        if all(m in morphs and morphs[m] in tokens for m in atoms):
            matches.append(f"{word} = " + " + ".join(atoms))
        else:
            # попытка поанглийски
            if all(a in tokens for a in atoms):
                matches.append(f"{word} = " + " + ".join(atoms))
    if not matches:
        matches = ["No matches found."]
    return matches

# UI: Перевод вперед
st.header("Forward: Star Script → English")
inp_f = st.text_input("Enter Star Script phrase:")
if st.button("Translate →"):
    results = translate_forward(inp_f.lower())
    for line in results:
        st.markdown(line)

st.write("---")
# UI: Перевод обратно
st.header("Reverse: English atoms → Star Script")
inp_r = st.text_input("Enter English atoms (e.g. object move water):")
if st.button("Translate ←"):
    results = translate_reverse(inp_r.lower())
    for line in results:
        st.write(line)