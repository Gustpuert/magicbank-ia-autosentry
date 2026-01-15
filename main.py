from core.scheduler import run_scheduler

# Importar detectores reales del repo
from detectors.derecho import DerechoDetector
from detectors.tributario import TributarioDetector
from detectors.marketing import MarketingDetector
from detectors.software import SoftwareDetector
from detectors.administracion import AdministracionDetector

def main():
    detectors = [
        DerechoDetector(),
        TributarioDetector(),
        MarketingDetector(),
        SoftwareDetector(),
        AdministracionDetector()
    ]

    print("[MagicBank IA AutoSentry] Inicio de ejecución")
    run_scheduler(detectors)
    print("[MagicBank IA AutoSentry] Ejecución finalizada")

if __name__ == "__main__":
    main()
