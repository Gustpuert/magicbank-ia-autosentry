# email.py
# MagicBank IA AutoSentry
# Envío de alertas automáticas por correo para eventos de ALTA RELEVANCIA

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from notifications.mail_config import MAIL_SETTINGS


def send_email_if_needed(event):
    """
    Envía un correo electrónico SOLO si el evento tiene relevancia 'high'.

    El evento debe contener al menos:
    - event.relevance
    - event.faculty
    - event.jurisdiction
    - event.document_type
    - event.title
    - event.publication_date
    - event.effective_date (opcional)
    - event.source_url
    - event.detected_at
    """

    # Filtro estricto de relevancia
    if event.relevance != "high":
        return

    subject = f"[MagicBank IA] Alerta de Alta Relevancia – {event.faculty.upper()}"

    body = f"""
Se ha detectado una novedad de ALTA RELEVANCIA en MagicBank.

FACULTAD: {event.faculty}
JURISDICCIÓN: {event.jurisdiction}
TIPO DE DOCUMENTO: {event.document_type}
TÍTULO: {event.title}

FECHA DE PUBLICACIÓN: {event.publication_date}
FECHA DE VIGENCIA: {event.effective_date or 'No especificada'}

FUENTE OFICIAL:
{event.source_url}

FECHA DE DETECCIÓN:
{event.detected_at}

⚠️ Esta es una NOTA AUTOMÁTICA.
No modifica módulos académicos.
Debe ser revisada por tutores MagicBank.

— MagicBank IA AutoSentry
""".strip()

    # Construcción del mensaje
    message = MIMEMultipart()
    message["From"] = MAIL_SETTINGS["sender_email"]
    message["To"] = MAIL_SETTINGS["receiver_email"]
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain", "utf-8"))

    try:
        # Conexión SMTP segura
        with smtplib.SMTP(MAIL_SETTINGS["smtp_server"], MAIL_SETTINGS["smtp_port"]) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(
                MAIL_SETTINGS["sender_email"],
                MAIL_SETTINGS["app_password"]
            )

            server.send_message(message)

    except Exception as e:
        # Log simple (puede reemplazarse por logging estructurado)
        print(f"[MagicBank IA AutoSentry] Error enviando correo: {e}")
