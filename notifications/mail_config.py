import os

# ==========================
# CONFIGURACIÓN DE CORREO
# ==========================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_REMITENTE = os.getenv("MAIL_USER")
EMAIL_PASSWORD = os.getenv("MAIL_APP_PASSWORD")

# Lista blanca de destinatarios permitidos
DESTINATARIOS_AUTORIZADOS = [
    "tucorreo@gmail.com",
    "alertas@tudominio.com"
]

def es_destino_valido(email: str) -> bool:
    """Evita envíos accidentales o no autorizados"""
    return email in DESTINATARIOS_AUTORIZADOS
