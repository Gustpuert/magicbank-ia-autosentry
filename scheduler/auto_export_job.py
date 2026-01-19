from export.auto_exporter import AutoHistoryExporter
from export.uploader import HistoryUploader


def run():
    exporter = AutoHistoryExporter()
    result = exporter.run()

    uploader = HistoryUploader()
    publish_result = uploader.upload(
        pdf_path=result["pdf"],
        signature_path=result["signature"]
    )

    print("[OK] Historial generado y publicado")
    print(f"PDF: {publish_result['pdf']}")
    print(f"Firma: {publish_result['signature']}")


if __name__ == "__main__":
    run()
