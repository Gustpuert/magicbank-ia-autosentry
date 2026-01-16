class BaseDetector:
    """
    Clase base para todos los detectores MagicBank IA AutoSentry.

    Cada detector concreto debe implementar el método detect()
    y devolver una lista de objetos DetectionEvent.
    """

    def detect(self):
        raise NotImplementedError("Detector no implementado")
