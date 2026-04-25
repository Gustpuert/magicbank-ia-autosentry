def evaluate_academic_impact(event):
    """
    Determina si un evento es relevante para enseñanza jurídica.
    """

    if not event or not event.title:
        return "low"

    title = event.title.lower()

    score = 0

    # 🔹 Tipo jurídico (base)
    if event.legal_type in ["ley", "sentencia"]:
        score += 3
    elif event.legal_type == "decreto":
        score += 2
    elif event.legal_type == "resolucion":
        score += 1

    # 🔹 Palabras de impacto estructural
    impact_keywords = [
        "reforma",
        "modifica",
        "deroga",
        "nuevo",
        "regula",
        "cambia",
        "estructura",
        "sistema"
    ]

    for k in impact_keywords:
        if k in title:
            score += 2

    # 🔹 Exclusión de ruido académico
    noise_keywords = [
        "boletín",
        "comunicado",
        "noticia",
        "evento",
        "foro",
        "conferencia"
    ]

    for k in noise_keywords:
        if k in title:
            score -= 2

    # 🔹 Resultado final
    if score >= 5:
        return "high"
    elif score >= 3:
        return "medium"

    return "low"
