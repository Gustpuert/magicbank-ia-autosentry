from core.pipeline import process_event

def run_scheduler(detectors):
    """
    Ejecuta todos los detectores registrados y procesa
    los eventos detectados mediante el pipeline MagicBank IA AutoSentry.
    """

    for detector in detectors:
        try:
            events = detector.detect()
        except Exception as e:
            print(f"[AutoSentry] Error en detector {detector.__class__.__name__}: {e}")
            continue

        for event in events:
            try:
                process_event(event)
            except Exception as e:
                print(f"[AutoSentry] Error procesando evento: {e}")
