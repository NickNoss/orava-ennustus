import os
import shutil
import zipfile
import subprocess
from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
OUTPUT_HTML = os.path.join(BASE_DIR, "outputs", "map.html")

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_algorithm():
    # Tyhjennä vanhat kuvat
    if os.path.exists(IMAGES_DIR):
        shutil.rmtree(IMAGES_DIR)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    uploaded_files = request.files.getlist("files")

    for file in uploaded_files:
        if not file.filename:
            continue

        filename = secure_filename(os.path.basename(file.filename))

        if filename.lower().endswith(".zip"):
            zip_path = os.path.join(DATA_DIR, "temp.zip")
            file.save(zip_path)
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(IMAGES_DIR)
        else:
            file.save(os.path.join(IMAGES_DIR, filename))

    # Hae CSV
    csv_file = request.files["csv_file"]
    csv_name = secure_filename(os.path.basename(csv_file.filename))
    csv_file.save(os.path.join(DATA_DIR, "detections.csv"))

    # Aja algoritmi
    try:
        subprocess.run(
            ["python", os.path.join(BASE_DIR, "main.py")],
            cwd=BASE_DIR,
            check=True,
        )
    except Exception as e:
        return f"Algoritmin ajo epäonnistui: {e}", 500

    if os.path.exists(OUTPUT_HTML):
        return send_file(OUTPUT_HTML)
    else:
        return "map.html ei löytynyt", 500




if __name__ == "__main__":
    app.run(debug=True)
