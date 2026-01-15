class BaseDetector:
    def __init__(self, sources):
        self.sources = sources

    def detect(self):
        """
        Debe ser implementado por cada detector específico.
        Debe devolver una lista de DetectionEvent.
        """
        raise NotImplementedError("Detector no implementado")