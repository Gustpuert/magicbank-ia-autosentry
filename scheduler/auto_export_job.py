from export.auto_exporter import AutoHistoryExporter


def run():
    exporter = AutoHistoryExporter()
    file_generated = exporter.run()
    print(f"[OK] Historial generado: {file_generated}")


if __name__ == "__main__":
    run()
