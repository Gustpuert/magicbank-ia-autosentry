import requests
from bs4 import BeautifulSoup
from datetime import datetime

from detectors.base import BaseDetector
from core.event import DetectionEvent


class DerechoDetector(BaseDetector):

    def detect(self):
        events = []

        print("[INFO] DerechoDetector iniciado")

        events += self.funcion_publica()
        events += self.diario_oficial()
        events += self.corte_constitucional()
        events += self.senado()
        events += self.dian()

        print(f"[INFO] DerechoDetector encontró {len(events)} eventos")

        return events


    def fetch(self, url):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print(f"[FETCH ERROR] {url}: {e}")
        return None


    # =========================
    # 🏛️ FUNCIÓN PÚBLICA
    # =========================
    def funcion_publica(self):
        url = "https://www.funcionpublica.gov.co/eva/es/gestornormativo"
        return self.parse_source(url, "CO", "derecho")


    # =========================
    # 📰 DIARIO OFICIAL
    # =========================
    def diario_oficial(self):
        url = "https://www.imprenta.gov.co/gacetap/gaceta.mostrar_gaceta?p_tipo=01&p_numero="
        return self.parse_source(url, "CO", "derecho")


    # =========================
    # ⚖️ CORTE CONSTITUCIONAL
    # =========================
    def corte_constitucional(self):
        url = "https://www.corteconstitucional.gov.co"
        return self.parse_source(url, "CO", "derecho")


    # =========================
    # 🏛️ SENADO
    # =========================
    def senado(self):
        url = "https://www.senado.gov.co"
        return self.parse_source(url, "CO", "derecho")


    # =========================
    # 💰 DIAN
    # =========================
    def dian(self):
        url = "https://www.dian.gov.co"
        return self.parse_source(url, "CO", "tributario")


    # =========================
    # 🔧 PARSER BASE CONTROLADO
    # =========================
    def parse_source(self, url, jurisdiction, faculty):
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.select("a")[:40]:
            title = tag.get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(
                    DetectionEvent(
                        faculty=faculty,
                        jurisdiction=jurisdiction,
                        source_url=url,
                        title=title,
                        document_type="Norma jurídica",
                        publication_date=datetime.utcnow().date().isoformat()
                    )
                )

        return events


    # =========================
    # ⚖️ FILTRO JURÍDICO BASE
    # =========================
    def is_legal_relevant(self, title):
        if not title:
            return False

        title = title.lower()

        keywords = [
            "ley",
            "decreto",
            "sentencia",
            "resolución",
            "acuerdo",
            "reforma",
            "estatuto",
            "código",
            "reglamenta",
            "tributario",
            "constitucional"
        ]

        return any(k in title for k in keywords)
