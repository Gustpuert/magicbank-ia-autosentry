from core.relevance import evaluate_relevance
from core.legal_classifier import classify_legal_type
from registry.store import store_event
from notifications.email import send_email_if_needed


def process_event(event):
    """
    Procesa un evento detectado aplicando:
    - Clasificación jurídica
    - Evaluación de relevancia
    - Persistencia
    - Notificación
    """

    if not event:
        print("[WARNING] Evento inválido")
        return

    try:
        # 🔹 1. Clasificar tipo jurídico
        event.legal_type = classify_legal_type(event.title)

        # 🔹 2. Evaluar relevancia
        event.relevance = evaluate_relevance(event)

        # 🔹 3. Guardar evento
        stored = store_event(event)

        # 🔹 4. Notificar solo si es nuevo
        if stored:
            send_email_if_needed(event)

        print(f"[EVENT] {event.title} | tipo={event.legal_type} | relevancia={event.relevance}")

    except Exception as e:
        print(f"[ERROR PIPELINE] {e}")
