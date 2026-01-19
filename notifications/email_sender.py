import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from notifications.mail_config import (
    MAIL_HOST,
    MAIL_PORT,
    MAIL_USER,
    MAIL_PASSWORD,
    MAIL_FROM,
    MAIL_TO
)


def enviar_correo(asunto: str, mensaje: str):
    """
    Envía un correo electrónico usando SMTP seguro (TLS)
    """

    msg = MIMEMultipart()
    msg["From"] = MAIL_FROM
    msg["To"] = MAIL_TO
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain", "utf-8"))

    try:
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USER, MAIL_PASSWORD)
            server.send_message(msg)

        print("📧 Correo enviado correctamente")

    except Exception as e:
        print("❌ Error enviando correo:", str(e))
        raise
