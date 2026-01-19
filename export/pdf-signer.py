from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, serialization
from cryptography.hazmat.backends import default_backend
from pathlib import Path


class PDFSigner:
    """
    Firma digitalmente un PDF usando clave privada RSA.
    """

    def __init__(self, private_key_path="certificates/magicbank_private.pem"):
        self.private_key_path = Path(private_key_path)

        if not self.private_key_path.exists():
            raise FileNotFoundError("Clave privada no encontrada.")

        with open(self.private_key_path, "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

    def sign_file(self, pdf_path: str):
        pdf_path = Path(pdf_path)

        with open(pdf_path, "rb") as f:
            data = f.read()

        signature = self.private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        signature_path = pdf_path.with_suffix(".sig")

        with open(signature_path, "wb") as sig:
            sig.write(signature)

        return signature_path
