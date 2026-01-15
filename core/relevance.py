def evaluate_relevance(event):
    high_keywords = [
        "reforma",
        "modificación",
        "nuevo",
        "vigencia",
        "actualización",
        "obligatorio",
        "impuesto",
        "tributario",
        "sentencia"
    ]

    critical_faculties = ["derecho", "contaduria"]

    title = event.title.lower()

    for keyword in high_keywords:
        if keyword in title:
            # Derecho y Contaduría elevan prioridad
            if event.faculty in critical_faculties:
                return "high"
            return "normal"

    return "normal"
