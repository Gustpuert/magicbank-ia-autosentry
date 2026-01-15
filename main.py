from scheduler import run_scheduler

# Importar detectores
from detectors.legal_colombia import LegalColombiaDetector
from detectors.tax_colombia import TaxColombiaDetector
from detectors.legal_canada import LegalCanadaDetector
from detectors.legal_usa import LegalUSADetector
from detectors.marketing_trends import MarketingTrendsDetector
from detectors.software_updates import SoftwareUpdatesDetector

def main():
    detectors = [
        LegalColombiaDetector(),
        TaxColombiaDetector(),
        LegalCanadaDetector(),
        LegalUSADetector(),
        MarketingTrendsDetector(),
        SoftwareUpdatesDetector()
    ]

    print("[MagicBank IA AutoSentry] Inicio de ejecución")
    run_scheduler(detectors)
    print("[MagicBank IA AutoSentry] Ejecución finalizada")

if __name__ == "__main__":
    main()
