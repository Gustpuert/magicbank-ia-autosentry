from core.relevance import evaluate_relevance
from core.legal_classifier import classify_legal_type
from core.academic_impact import evaluate_academic_impact
from registry.store import store_event
from notifications.email import send_email_if_needed


def process_event(event):
    """
    Pipeline inteligente de MagicBank:
    - Clasificación jurídica
    - Evaluación de relevancia
    - Evaluación de impacto académico
    - Decisión automática de almacenamiento y notificación
    """

    if not event:
        print("[WARNING] Evento inválido")
        return

    try:
        # 🔹 1. Clasificación jurídica
        event.legal_type = classify_legal_type(event.title)

        # 🔹 2. Relevancia jurídica
        event.relevance = evaluate_relevance(event)

        # 🔥 3. Impacto académico (NUEVO)
        academic_impact = evaluate_academic_impact(event)

        # 🔥 4. FILTRO FINAL (CLAVE DEL SISTEMA)
        if academic_impact == "low":
            print(f"[IGNORED] Bajo impacto académico: {event.title}")
            return

        # 🔹 5. Persistencia
        stored = store_event(event)

        # 🔹 6. Notificación (solo alto impacto)
        if stored and academic_impact == "high":
            send_email_if_needed(event)

        print(
            f"[EVENT] {event.title} | "
            f"tipo={event.legal_type} | "
            f"relevancia={event.relevance} | "
            f"impacto_academico={academic_impact}"
        )

    except Exception as e:
        print(f"[ERROR PIPELINE] {e}")
