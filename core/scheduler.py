from registry.store import store_if_changed
from notifications.email_sender import enviar_correo
from datetime import datetime


def run_scheduler(detectors):
    nuevos = []

    for detector in detectors:
        try:
            resultados = detector.detect()
            for r in resultados:
                if store_if_changed(r):
                    nuevos.append(r)
        except Exception as e:
            print(f"[ERROR] {detector.__class__.__name__}: {e}")

    if nuevos:
        resumen = generar_resumen(nuevos)
        enviar_correo(
            destinatario="magicbankia@gmail.com",
            asunto="📡 MagicBank — Actualización Oficial Detectada",
            mensaje=resumen
        )


def generar_resumen(resultados):
    texto = []
    texto.append("📘 ACTUALIZACIONES OFICIALES DETECTADAS\n")

    for r in resultados:
        texto.append(
            f"- {r.get('pais')} | {r.get('rama')} | {r.get('entidad')}"
        )

    texto.append("\nSistema MagicBank IA")
    texto.append(f"Fecha UTC: {datetime.utcnow().isoformat()}")

    return "\n".join(texto)
