from export.auto_exporter import AutoHistoryExporter
from export.uploader import HistoryUploader
from export.mailer import HistoryMailer
import os


def run():
    exporter = AutoHistoryExporter()
    result = exporter.run()

    uploader = HistoryUploader()
    published = uploader.upload(
        pdf_path=result["pdf"],
        signature_path=result["signature"]
    )

    mailer = HistoryMailer(
        smtp_server="smtp.gmail.com",
        smtp_port=465,
        email_sender=os.getenv("MAIL_SENDER"),
        email_password=os.getenv("MAIL_PASSWORD"),
        email_receiver=os.getenv("MAIL_RECEIVER")
    )

    mailer.send(
        pdf_path=published["pdf"],
        signature_path=published["signature"]
    )

    print("[OK] PDF generado, firmado, publicado y enviado por correo.")


if __name__ == "__main__":
    run()
