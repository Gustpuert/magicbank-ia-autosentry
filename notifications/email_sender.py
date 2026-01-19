import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASSWORD = os.getenv("MAIL_APP_PASSWORD")
MAIL_TO = os.getenv("MAIL_RECEIVER")


def enviar_correo(destinatario, asunto, mensaje):
    if not MAIL_USER or not MAIL_PASSWORD:
        raise RuntimeError("Credenciales de correo no configuradas")

    msg = MIMEMultipart()
    msg["From"] = MAIL_USER
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain", "utf-8"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(MAIL_USER, MAIL_PASSWORD)
        server.send_message(msg)

    print("📧 Correo enviado correctamente")
