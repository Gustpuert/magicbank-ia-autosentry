def classify_legal_type(title: str):
    """
    Clasifica el tipo de norma jurídica basado en el título.
    """

    if not title:
        return "otro"

    title = title.lower()

    if "constitución" in title:
        return "constitucional"

    if "ley" in title:
        return "ley"

    if "decreto" in title:
        return "decreto"

    if "resolución" in title or "resolucion" in title:
        return "resolucion"

    if "sentencia" in title:
        return "sentencia"

    return "otro"
