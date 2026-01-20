# GEL AI Subs — Whisper Backend
# Simple HTTP API for subtitle generation

from flask import Flask, request, jsonify
import whisper
import os
import hashlib
from flask import send_from_directory

# Load Whisper model
model = whisper.load_model("base")

DATA_DIR = "data"
SUB_DIR = os.path.join(DATA_DIR, "subs")

os.makedirs(SUB_DIR, exist_ok=True)

def make_job_hash(path, lang):
    return hashlib.md5(f"{path}_{lang}".encode("utf-8")).hexdigest()

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.get_json(force=True)

    video_path = data.get("path")
    lang = data.get("lang", "auto")

    if not video_path:
        return jsonify({"error": "Missing video path"}), 400

    job = make_job_hash(video_path, lang)
    srt_path = os.path.join(SUB_DIR, f"{job}.srt")

    # Cache hit
    if os.path.exists(srt_path):
        return jsonify({
    "cached": True,
    "srt": f"/subs/{os.path.basename(srt_path)}"
})

    # Transcribe
    result = model.transcribe(
        video_path,
        language=None if lang == "auto" else lang
    )

    # Write SRT
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result["segments"], start=1):
            f.write(f"{i}\n")
            f.write(f"{seg['start']:.2f} --> {seg['end']:.2f}\n")
            f.write(seg["text"].strip() + "\n\n")

    return jsonify({
    "cached": False,
    "srt": f"/subs/{os.path.basename(srt_path)}"
})
    
@app.route("/subs/<filename>", methods=["GET"])
def download_sub(filename):
    return send_from_directory(SUB_DIR, filename, as_attachment=False)

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
