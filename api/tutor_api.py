from tutors.lasttutorsengine import LastTutorEngine


class TutorAPI:
    """
    API interna para interactuar con los tutores de MagicBank.
    """

    def __init__(self, area: str):
        self.tutor = LastTutorEngine(area)

    def consultar(self, pregunta: str) -> dict:
        """
        Devuelve una respuesta del tutor basada únicamente
        en información validada.
        """

        respuesta = self.tutor.respond(pregunta)

        return {
            "status": "ok",
            "area": self.tutor.area,
            "pregunta": pregunta,
            "respuesta": respuesta
        }


# =========================
# USO DIRECTO (opcional)
# =========================

if __name__ == "__main__":
    api = TutorAPI(area="Derecho Constitucional")
    resultado = api.consultar(
        "¿Qué cambios recientes existen en la normativa vigente?"
    )
    print(resultado)
