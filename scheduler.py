def run_scheduler(detectors):
    for detector in detectors:
        events = detector.detect()
        for event in events:
            from core.pipeline import process_event
            process_event(event)