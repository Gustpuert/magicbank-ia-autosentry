from core.pipeline import process_event


def run_scheduler(detectors):
    """
    Ejecuta todos los detectores y procesa los eventos.
    """

    if not detectors:
        print("[WARNING] No hay detectores configurados")
        return

    total_events = 0

    for detector in detectors:
        try:
            print(f"[INFO] Ejecutando detector: {detector.__class__.__name__}")

            events = detector.detect()

            if not events:
                print(f"[INFO] Sin eventos en {detector.__class__.__name__}")
                continue

            for event in events:
                process_event(event)
                total_events += 1

        except Exception as e:
            print(f"[ERROR DETECTOR] {detector.__class__.__name__}: {e}")

    print(f"[FINAL] Total eventos procesados: {total_events}")
