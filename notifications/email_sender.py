import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviar_correo(asunto: str, mensaje: str):
    remitente = os.getenv("MAIL_SENDER")
    destinatario = os.getenv("MAIL_RECEIVER")
    password = os.getenv("MAIL_APP_PASSWORD")

    if not remitente or not destinatario or not password:
        raise ValueError("Variables de entorno de correo no configuradas")

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(remitente, password)
        server.send_message(msg)
