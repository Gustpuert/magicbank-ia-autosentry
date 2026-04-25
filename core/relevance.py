from core.legal_classifier import classify_legal_type


def evaluate_relevance(event):
    """
    Evalúa la relevancia jurídica del evento basado en:
    - Tipo de norma
    - Palabras clave jurídicas
    - Facultad afectada
    """

    if not event or not event.title:
        return "low"

    title = event.title.lower()

    score = 0

    # 🔹 1. Clasificación jurídica
    tipo = classify_legal_type(title)

    if tipo == "sentencia":
        score += 4
    elif tipo == "ley":
        score += 3
    elif tipo == "decreto":
        score += 2
    elif tipo == "resolucion":
        score += 1

    # 🔹 2. Palabras clave de impacto
    keywords = [
        "reforma",
        "modifica",
        "deroga",
        "vigencia",
        "obligatorio",
        "reglamenta",
        "sustituye"
    ]

    for k in keywords:
        if k in title:
            score += 2

    # 🔹 3. Facultades críticas
    if event.faculty in ["derecho", "tributario"]:
        score += 2

    # 🔹 4. Resultado final
    if score >= 7:
        return "critical"
    elif score >= 4:
        return "high"
    elif score >= 2:
        return "normal"

    return "low"
