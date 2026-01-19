from notifications.email_sender import enviar_correo
from datetime import datetime


def run_scheduler(detectors):
    resultados = []

    for detector in detectors:
        try:
            detecciones = detector.detect()
            if detecciones:
                resultados.extend(detecciones)
        except Exception as e:
            print(f"[ERROR] Detector {detector.__class__.__name__}: {e}")

    # Si hay resultados, enviar correo
    if resultados:
        resumen = generar_resumen(resultados)
        enviar_correo(
            destinatario="tucorreo@gmail.com",
            asunto="📡 MagicBank – Nuevas detecciones",
            mensaje=resumen
        )

    return resultados


def generar_resumen(resultados):
    salida = []
    salida.append("Se detectaron nuevas actualizaciones:\n")

    for r in resultados:
        salida.append(
            f"- {r.get('pais')} | {r.get('rama')} | {r.get('entidad')} | {r.get('fuente')}"
        )

    salida.append("\nGenerado automáticamente por MagicBank IA.")
    salida.append(f"Fecha: {datetime.utcnow().isoformat()} UTC")

    return "\n".join(salida)
