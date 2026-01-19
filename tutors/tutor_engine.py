from core.context_loader import load_authorized_context


class TutorEngine:
    """
    Motor base de tutores IA de MagicBank.
    """

    def __init__(self, area: str):
        self.area = area
        self.contexto = ""

    def load_context(self):
        """
        Carga únicamente información validada y autorizada.
        """
        self.contexto = load_authorized_context(self.area)

    def respond(self, question: str) -> str:
        """
        Simula la respuesta del tutor usando solo contexto autorizado.
        """

        if not self.contexto:
            self.load_context()

        response = f"""
        CONTEXTO OFICIAL DISPONIBLE:
        {self.contexto}

        PREGUNTA DEL USUARIO:
        {question}

        RESPUESTA DEL TUTOR:
        (Basada exclusivamente en el contexto oficial anterior)
        """

        return response.strip()
