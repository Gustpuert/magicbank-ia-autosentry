import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from notifications.mail_config import (
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_REMITENTE,
    EMAIL_PASSWORD,
    es_destino_valido
)

def enviar_correo(destinatario: str, asunto: str, mensaje: str):
    if not es_destino_valido(destinatario):
        raise ValueError("❌ Destinatario NO autorizado")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMITENTE
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"📧 Correo enviado correctamente a {destinatario}")

    except Exception as e:
        print("❌ Error enviando correo:", str(e))
        raise
