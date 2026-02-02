from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from backend.resume_engine import ResumeProcessor

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

processor = ResumeProcessor()

def calculate_scores(data):
    scores = {
        "formatting": 20 if data["summary"]["found"] else 10,
        "content": 40 if data["education"]["found"] else 20,
        "experience": 60 if data["experience"]["found"] else 20,
        "skills": min(len(data["skills"]["technical"]) * 10, 100)
    }
    overall = sum(scores.values()) // 4
    return overall, scores

@app.route("/api/upload", methods=["POST"])
def upload_resume():
    file = request.files.get("resume")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = processor.extract_text_from_pdf(path)
    parsed = pro
