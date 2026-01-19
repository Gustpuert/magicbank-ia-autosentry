import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime


# ==============================
# CONFIGURACIÓN PRINCIPAL
# ==============================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

MAIL_SENDER = os.getenv("MAIL_SENDER")
MAIL_PASSWORD = os.getenv("MAIL_APP_PASSWORD")
MAIL_RECEIVER = os.getenv("MAIL_RECEIVER")


# ==============================
# FUNCIÓN PRINCIPAL
# ==============================

def enviar_correo(asunto: str, mensaje: str):
    if not MAIL_SENDER or not MAIL_PASSWORD or not MAIL_RECEIVER:
        raise ValueError("❌ Faltan variables de entorno para el envío de correo.")

    msg = MIMEMultipart()
    msg["From"] = MAIL_SENDER
    msg["To"] = MAIL_RECEIVER
    msg["Subject"] = asunto

    cuerpo = f"""
MagicBank IA — Sistema Automático de Notificación

Fecha: {datetime.utcnow().isoformat()} UTC

{mensaje}

---
Este mensaje fue generado automáticamente.
No responder.
"""

    msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MAIL_SENDER, MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("✅ Correo enviado correctamente.")

    except Exception as e:
        print("❌ Error enviando correo:")
        print(str(e))


# ==============================
# EJECUCIÓN DIRECTA (TEST)
# ==============================

if __name__ == "__main__":
    enviar_correo(
        asunto="📡 MagicBank AutoSentry – Ejecución correcta",
        mensaje="El sistema se ejecutó correctamente y no se detectaron errores."
    )
