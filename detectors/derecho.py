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
        events += self.corte_constitucional()
        events += self.diario_oficial()
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
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("div.views-row")

        for row in rows[:20]:
            title_tag = row.select_one("h3, h2, a")

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(self.build_event(title, url, "derecho"))

        return events


    # =========================
    # ⚖️ CORTE CONSTITUCIONAL
    # =========================
    def corte_constitucional(self):
        url = "https://www.corteconstitucional.gov.co/relatoria/"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("table tr")

        for row in rows[:20]:
            cols = row.find_all("td")

            if len(cols) < 2:
                continue

            title = cols[1].get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(self.build_event(title, url, "derecho"))

        return events


    # =========================
    # 📰 DIARIO OFICIAL
    # =========================
    def diario_oficial(self):
        url = "https://www.imprenta.gov.co"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all(["a", "p", "span"])[:50]:
            text = tag.get_text(strip=True)

            if not text:
                continue

            if self.is_legal_relevant(text):
                events.append(self.build_event(text, url, "derecho"))

        return events


    # =========================
    # 🏛️ SENADO
    # =========================
    def senado(self):
        url = "https://www.senado.gov.co/index.php/el-senado/noticias"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")
        articles = soup.select("article, div.views-row")

        for article in articles[:20]:
            title_tag = article.find("a")

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(self.build_event(title, url, "derecho"))

        return events


    # =========================
    # 💰 DIAN (TRIBUTARIO)
    # =========================
    def dian(self):
        url = "https://www.dian.gov.co/Prensa/Paginas/Normatividad.aspx"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("table tr")

        for row in rows[:20]:
            cols = row.find_all("td")

            if len(cols) < 2:
                continue

            title = cols[1].get_text(strip=True)

            if self.is_legal_relevant(title):
                events.append(self.build_event(title, url, "tributario"))

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


    # =========================
    # 🏗️ CREACIÓN DE EVENTO
    # =========================
    def build_event(self, title, source, faculty):
        return DetectionEvent(
            faculty=faculty,
            jurisdiction="CO",
            source_url=source,
            title=title,
            document_type="Norma jurídica",
            publication_date=datetime.utcnow().date().isoformat()
        )
