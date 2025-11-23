import os
import shutil
import zipfile
import subprocess
from flask import Flask, request, send_file, render_template

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

    # Tyhjennä data/images ja data/detections.csv
    if os.path.exists(IMAGES_DIR):
        shutil.rmtree(IMAGES_DIR)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # --- 1) Käsittele kuvat ---
    images = request.files.getlist("images")
    if len(images) == 1 and images[0].filename.lower().endswith(".zip"):
        zip_path = os.path.join(DATA_DIR, "images.zip")
        images[0].save(zip_path)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(IMAGES_DIR)
    else:
        for img in images:
            if img.filename:
                img.save(os.path.join(IMAGES_DIR, img.filename))

    # --- 2) Käsittele CSV ---
    csv_file = request.files["csv_file"]
    csv_file.save(os.path.join(DATA_DIR, "detections.csv"))

    # --- 3) Aja main.py ---
    try:
        subprocess.run(
            ["python", os.path.join(BASE_DIR, "main.py")],
            cwd=BASE_DIR,
            check=True
        )
    except Exception as e:
        return f"Algoritmin ajo epäonnistui: {e}", 500

    # --- 4) Palauta HTML-tulos ---
    if os.path.exists(OUTPUT_HTML):
        return send_file(OUTPUT_HTML)
    else:
        return "map.html ei löytynyt", 500

if __name__ == "__main__":
    app.run(debug=True)
