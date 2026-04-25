import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
import json
import os

from core.event import DetectionEvent

HISTORY_FILE = "legal_history.json"


class DerechoDetector:

    # =========================
    # 🚀 EJECUCIÓN PRINCIPAL
    # =========================
    def detect(self):
        print("[INFO] DerechoDetector iniciado")

        history = self.load_history()

        events = []
        events += self.diario_oficial()         # 🔥 fuente principal
        events += self.funcion_publica()
        events += self.corte_constitucional()
        events += self.consejo_estado()
        events += self.senado()
        events += self.presidencia()
        events += self.dian()

        events = self.filter_relevant(events)
        events = self.remove_duplicates(events)

        new_events = []

        for e in events:
            key = self.hash_event(e)

            if key not in history:
                history.add(key)
                new_events.append(e)

        self.save_history(history)

        print(f"[INFO] Nuevos eventos: {len(new_events)}")

        for event in new_events:
            self.send_to_tutor(event)

        return new_events


    # =========================
    # 🌐 FETCH
    # =========================
    def fetch(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print(f"[ERROR] {url}: {e}")
        return None


    # =========================
    # 🏛️ FUENTES OFICIALES
    # =========================

    def diario_oficial(self):
        url = "https://www.imprenta.gov.co"
        html = self.fetch(url)
        events = []

        if not html:
            return events

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all(["a", "p", "span"])[:60]:
            text = tag.get_text(strip=True)

            if len(text) > 15:
                events.append(self.build_event(text, url))

        return events


    def funcion_publica(self):
        return self.parse_links("https://www.funcionpublica.gov.co/eva/es/gestornormativo")


    def corte_constitucional(self):
        return self.parse_table("https://www.corteconstitucional.gov.co/relatoria/")


    def consejo_estado(self):
        return self.parse_links("https://www.consejodeestado.gov.co/boletines/")


    def senado(self):
        return self.parse_links("https://www.senado.gov.co/index.php/el-senado/noticias")


    def presidencia(self):
        return self.parse_links("https://dapre.presidencia.gov.co/normativa/normativa")


    def dian(self):
        return self.parse_table("https://www.dian.gov.co/Prensa/Paginas/Normatividad.aspx")


    # =========================
    # 🔍 PARSERS
    # =========================

    def parse_links(self, url):
        html = self.fetch(url)
        results = []

        if not html:
            return results

        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")

        for link in links[:40]:
            title = link.get_text(strip=True)

            if len(title) > 12:
                results.append(self.build_event(title, url))

        return results


    def parse_table(self, url):
        html = self.fetch(url)
        results = []

        if not html:
            return results

        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("table tr")

        for row in rows[:40]:
            cols = row.find_all("td")

            if len(cols) < 2:
                continue

            title = cols[1].get_text(strip=True)

            if len(title) > 12:
                results.append(self.build_event(title, url))

        return results


    # =========================
    # 🎯 FILTRO JURÍDICO
    # =========================

    def filter_relevant(self, events):
        keywords = [
            "ley",
            "decreto",
            "sentencia",
            "resolución",
            "acuerdo",
            "reforma",
            "estatuto",
            "código"
        ]

        blacklist = [
            "proyecto",
            "noticia",
            "evento",
            "foro",
            "convocatoria"
        ]

        filtered = []

        for e in events:
            title = e.title.lower()

            if any(b in title for b in blacklist):
                continue

            if any(k in title for k in keywords):
                filtered.append(e)

        return filtered


    # =========================
    # 🔁 DEDUPLICACIÓN
    # =========================

    def remove_duplicates(self, events):
        seen = set()
        unique = []

        for e in events:
            key = self.hash_event(e)

            if key not in seen:
                seen.add(key)
                unique.append(e)

        return unique


    # =========================
    # 🧠 HISTORIAL
    # =========================

    def load_history(self):
        if not os.path.exists(HISTORY_FILE):
            return set()

        with open(HISTORY_FILE, "r") as f:
            return set(json.load(f))


    def save_history(self, history):
        with open(HISTORY_FILE, "w") as f:
            json.dump(list(history), f)


    def hash_event(self, event):
        return hashlib.md5(event.title.lower().strip().encode()).hexdigest()


    # =========================
    # 🏗️ EVENTO
    # =========================

    def build_event(self, title, source):
        return DetectionEvent(
            faculty="derecho",
            jurisdiction="CO",
            source_url=source,
            title=title,
            document_type="Norma jurídica",
            publication_date=datetime.utcnow().date().isoformat()
        )


    # =========================
    # 🎓 INTEGRACIÓN CON TUTOR
    # =========================

    def send_to_tutor(self, event):
        module = self.classify_module(event.title)

        print("\n🎓 [TUTOR ACTIVADO]")
        print(f"📚 Norma: {event.title}")
        print(f"📌 Módulo: {module}")

        # 🔥 AQUÍ SE CONECTA TU TUTOR REAL
        # tutor.update(module, event)


    # =========================
    # 🧠 CURADURÍA
    # =========================

    def classify_module(self, title):
        title = title.lower()

        if "constitución" in title or "ley" in title:
            return "Módulo 2 – Derecho Constitucional"

        if "sentencia" in title:
            return "Módulo 4 – Jurisprudencia / Penal"

        if "decreto" in title or "resolución" in title:
            return "Módulo 5 – Derecho Administrativo"

        if "tributario" in title or "impuesto" in title:
            return "Módulo 7 – Derecho Comercial / Tributario"

        return "Revisión general"
