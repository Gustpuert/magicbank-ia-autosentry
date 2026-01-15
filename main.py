from core.scheduler import run_scheduler

# Importar detectores reales según el repo
from detectors.derecho import DerechoDetector
from detectors.tributario import TributarioDetector
from detectors.administracion import AdministracionDetector
from detectors.marketing import MarketingDetector
from detectors.software import SoftwareDetector


def main():
    detectors = [
        DerechoDetector(),
        TributarioDetector(),
        AdministracionDetector(),
        MarketingDetector(),
        SoftwareDetector()
    ]

    print("[MagicBank IA AutoSentry] Inicio de ejecución")
    run_scheduler(detectors)
    print("[MagicBank IA AutoSentry] Ejecución finalizada")


if __name__ == "__main__":
    main()
