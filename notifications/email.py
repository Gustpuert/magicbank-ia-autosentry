from notifications.email_sender import enviar_correo


def notificar_deteccion(resumen: str):
    asunto = "🛰️ MagicBank – Nueva detección jurídica"
    cuerpo = f"""
Se ha ejecutado el sistema MagicBank AutoSentry.

Resumen:
---------------------------------
{resumen}

Este correo fue generado automáticamente.
"""

    enviar_correo(asunto, cuerpo)
