from core.validator import validate_event
from registry.store import store_if_changed
from notifications.email_sender import enviar_correo
from datetime import datetime


def run_scheduler(detectors):
    eventos_validos = []

    for detector in detectors:
        try:
            resultados = detector.detect()

            for evento in resultados:
                validado = validate_event(evento)
                if validado:
                    eventos_validos.append(validado)

        except Exception as e:
            print(f"[ERROR] Detector {detector.__class__.__name__}: {e}")

    # Solo si hay cambios reales se guarda y se notifica
    if store_if_changed(eventos_validos):
        resumen = generar_resumen(eventos_validos)
        enviar_correo(
            destinatario="tucorreo@gmail.com",
            asunto="📡 MagicBank – Actualización oficial detectada",
            mensaje=resumen
        )

    return eventos_validos


def generar_resumen(eventos):
    salida = []
    salida.append("Se detectaron actualizaciones oficiales:\n")

    for e in eventos:
        salida.append(
            f"- {e['pais']} | {e['rama']} | {e['entidad']} | {e['fuente']}"
        )

    salida.append("\nFuente: MagicBank AutoSentry")
    salida.append(f"Fecha UTC: {datetime.utcnow().isoformat()}")

    return "\n".join(salida)
