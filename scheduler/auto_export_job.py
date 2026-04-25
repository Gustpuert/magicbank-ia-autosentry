from export.auto_exporter import AutoHistoryExporter
from export.uploader import HistoryUploader
from export.mailer import HistoryMailer
import os


def run():
    try:
        print("[INFO] Iniciando proceso de exportación...")

        # 🔹 1. Exportar historial
        exporter = AutoHistoryExporter()
        result = exporter.run()

        if not result or "pdf" not in result:
            print("[ERROR] Falló la exportación del historial")
            return

        print("[OK] Exportación completada")

        # 🔹 2. Subir archivo
        uploader = HistoryUploader()
        published = uploader.upload(
            pdf_path=result["pdf"],
            signature_path=result.get("signature")
        )

        if not published or "pdf" not in published:
            print("[ERROR] Falló la subida del archivo")
            return

        print("[OK] Publicación completada")

        # 🔹 3. Enviar correo
        mailer = HistoryMailer(
            smtp_server="smtp.gmail.com",
            smtp_port=465,
            email_sender=os.getenv("MAIL_SENDER"),
            email_password=os.getenv("MAIL_APP_PASSWORD"),  # 🔥 CORRECTO
            email_receiver=os.getenv("MAIL_RECEIVER")
        )

        mailer.send(
            pdf_path=published["pdf"],
            signature_path=published.get("signature")
        )

        print("[OK] Correo enviado correctamente")

        print("[FINAL] Proceso completo: exportado, firmado, publicado y enviado")

    except Exception as e:
        print("[ERROR GENERAL]", str(e))


if __name__ == "__main__":
    run()
