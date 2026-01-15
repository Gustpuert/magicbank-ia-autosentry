def evaluate_relevance(event):
    """
    Clasifica automáticamente la relevancia del evento.
    """

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

    title_lower = event.title.lower()

    for keyword in high_keywords:
        if keyword in title_lower:
            return "high"

    return "normal"