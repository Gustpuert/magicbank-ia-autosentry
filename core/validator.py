from datetime import datetime

# ==============================
# FUENTES OFICIALES AUTORIZADAS
# ==============================

OFFICIAL_SOURCES = {
    "colombia": [
        "corteconstitucional.gov.co",
        "consejodeestado.gov.co",
        "congreso.gov.co",
        "presidencia.gov.co",
        "dian.gov.co",
        "minjusticia.gov.co"
    ],
    "usa": [
        "supremecourt.gov",
        "federalregister.gov",
        "justice.gov",
        "irs.gov"
    ],
    "canada": [
        "justice.gc.ca",
        "scc-csc.ca"
    ],
    "global": [
        "openai.com",
        "developer.openai.com"
    ]
}

# ==============================
# FILTRO PRINCIPAL
# ==============================

def validate_event(event: dict) -> dict | None:
    """
    Recibe un evento detectado y decide si puede alimentar a los tutores.
    Devuelve el evento validado o None si es rechazado.
    """

    if not _is_official_source(event):
        return None

    if not _has_minimum_fields(event):
        return None

    if not _is_relevant(event):
        return None

    return _normalize_event(event)


# ==============================
# VALIDACIONES INTERNAS
# ==============================

def _is_official_source(event: dict) -> bool:
    url = event.get("fuente", "").lower()

    for group in OFFICIAL_SOURCES.values():
        if any(domain in url for domain in group):
            return True

    return False


def _has_minimum_fields(event: dict) -> bool:
    required = ["pais", "rama", "entidad", "fuente"]
    return all(field in event and event[field] for field in required)


def _is_relevant(event: dict) -> bool:
    """
    Decide si el cambio tiene impacto académico real
    """

    keywords = [
        "ley",
        "decreto",
        "resolución",
        "sentencia",
        "norma",
        "reglamento",
        "modificación",
        "actualización"
    ]

    text = " ".join(str(v).lower() for v in event.values())

    return any(word in text for word in keywords)


def _normalize_event(event: dict) -> dict:
    """
    Devuelve el evento listo para consumo por tutores
    """

    return {
        "fecha": datetime.utcnow().isoformat(),
        "pais": event["pais"],
        "rama": event["rama"],
        "entidad": event["entidad"],
        "fuente": event["fuente"],
        "estado": "AUTORIZADO",
        "tipo": "OFICIAL"
    }
