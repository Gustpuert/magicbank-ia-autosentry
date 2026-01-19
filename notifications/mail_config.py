import os

# ================================
# CONFIGURACIÓN DE CORREO
# ================================

MAIL_HOST = "smtp.gmail.com"
MAIL_PORT = 587

MAIL_USER = os.getenv("MAIL_APP_USER")
MAIL_PASSWORD = os.getenv("MAIL_APP_PASSWORD")

MAIL_FROM = MAIL_USER
MAIL_TO = os.getenv("MAIL_TO", MAIL_USER)

if not MAIL_USER or not MAIL_PASSWORD:
    raise RuntimeError("❌ Variables de entorno MAIL_APP_USER o MAIL_APP_PASSWORD no definidas")
