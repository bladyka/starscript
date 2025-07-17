def semantic_translate(word):
    word_lower = word.lower()
    if word_lower in dynamic_dict:
        return dynamic_dict[word_lower], "Cached translation"

    # Сначала проверка прямого совпадения
    if word_lower in BASE_CONCEPTS:
        return BASE_CONCEPTS[word_lower], "Direct base concept match"

    # Семантический поиск
    query_emb = model.encode(word_lower, convert_to_tensor=True)
    hits = util.semantic_search(query_emb, base_embeddings, top_k=3)[0]

    threshold = 0.5
    parts = []
    explanation = []
    for hit in hits:
        if hit['score'] >= threshold:
            concept = base_phrases[hit['corpus_id']]
            parts.append(BASE_CONCEPTS[concept])
            explanation.append(f"{concept} ({hit['score']:.2f})")

    if not parts:
        hash_key = hashlib.md5(word_lower.encode()).hexdigest()[:4]
        alien_word = f"???-{hash_key}"
        dynamic_dict[word_lower] = alien_word
        save_dynamic_dict(dynamic_dict)
        return alien_word, "No similar concepts found"

    alien_word = "-".join(sorted(set(parts)))
    dynamic_dict[word_lower] = alien_word
    save_dynamic_dict(dynamic_dict)
    return alien_word, " + ".join(explanation)
