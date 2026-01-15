from core.relevance import evaluate_relevance
from registry.store import store_event
from notifications.email import send_email_if_needed

def process_event(event):
    # 1. Evaluar relevancia
    event.relevance = evaluate_relevance(event)

    # 2. Registrar evento
    store_event(event)

    # 3. Notificar si aplica
    send_email_if_needed(event)