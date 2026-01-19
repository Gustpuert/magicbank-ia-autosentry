from flask import Flask, render_template, send_file
from export.pdf_generator import PDFHistoryGenerator
from pathlib import Path

app = Flask(__name__)

EXPORT_PATH = Path("exports")
EXPORT_PATH.mkdir(exist_ok=True)

@app.route("/admin/history", methods=["GET"])
def history_panel():
    return render_template("history.html")


@app.route("/admin/history/export", methods=["GET"])
def export_history_pdf():
    pdf_path = EXPORT_PATH / "historial_magicbank.pdf"

    generator = PDFHistoryGenerator()
    generator.generate_pdf(str(pdf_path))

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="historial_magicbank.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True, port=9000)
