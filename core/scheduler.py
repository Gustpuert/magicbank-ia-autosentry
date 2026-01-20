from registry.store import store_if_changed
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

    if not resultados:
        print("[INFO] No hay cambios detectados.")
        return

    # Guardar solo si hay cambios reales
    changed = store_if_changed(resultados)

    if not changed:
        print("[INFO] No hay cambios nuevos. No se envía correo.")
        return

    resumen = generar_resumen(resultados)

    enviar_correo(
        destinatario="magicbankia@gmail.com",
        asunto="📡 MagicBank – Actualización oficial detectada",
        mensaje=resumen
    )

    print("[OK] Actualización registrada y correo enviado.")


def generar_resumen(resultados):
    salida = []
    salida.append("📘 ACTUALIZACIÓN OFICIAL DETECTADA\n")

    for r in resultados:
        salida.append(
            f"- {r.get('pais')} | {r.get('rama')} | {r.get('entidad')}"
        )

    salida.append("\nSistema: MagicBank IA AutoSentry")
    salida.append(f"Fecha: {datetime.utcnow().isoformat()} UTC")

    return "\n".join(salida)
