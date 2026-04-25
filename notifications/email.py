import smtplib
from email.mime.text import MIMEText
import os


def send_email_if_needed(event):
    """
    Envía correo solo si el evento tiene relevancia alta o crítica.
    Incluye información jurídica enriquecida.
    """

    if not event:
        return

    if event.relevance not in ["high", "critical"]:
        return

    try:
        sender = os.getenv("MAIL_SENDER")
        password = os.getenv("MAIL_APP_PASSWORD")
        receiver = os.getenv("MAIL_RECEIVER")

        if not sender or not password or not receiver:
            print("[EMAIL WARNING] Variables de entorno incompletas")
            return

        message_body = f"""
📡 MagicBank IA — Actualización Jurídica Detectada

Tipo jurídico: {event.legal_type}
Relevancia: {event.relevance.upper()}

Título:
{event.title}

Fuente:
{event.source_url}

Jurisdicción:
{event.jurisdiction}

Fecha detección:
{event.detected_at}

— Sistema AutoSentry MagicBank
"""

        msg = MIMEText(message_body)
        msg["Subject"] = f"📡 [{event.relevance.upper()}] Actualización Jurídica"
        msg["From"] = sender
        msg["To"] = receiver

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        print("[EMAIL] Notificación enviada")

    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
