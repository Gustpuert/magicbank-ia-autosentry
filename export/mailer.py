import smtplib
from email.message import EmailMessage
from pathlib import Path


class HistoryMailer:
    """
    Envía automáticamente el PDF firmado del historial.
    """

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        email_sender: str,
        email_password: str,
        email_receiver: str
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_sender = email_sender
        self.email_password = email_password
        self.email_receiver = email_receiver

    def send(self, pdf_path: str, signature_path: str):
        msg = EmailMessage()
        msg["Subject"] = "Magic Bank — Historial Académico Firmado"
        msg["From"] = self.email_sender
        msg["To"] = self.email_receiver

        msg.set_content(
            "Adjunto se envía el historial académico oficial de Magic Bank,\n"
            "generado y firmado automáticamente por el sistema.\n\n"
            "Este documento es válido para auditoría y control institucional."
        )

        with open(pdf_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=Path(pdf_path).name
            )

        with open(signature_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=Path(signature_path).name
            )

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.email_sender, self.email_password)
            server.send_message(msg)
