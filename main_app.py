from flask import send_from_directory
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from resume_engine import ResumeProcessor

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
@app.route("/")
def serve_frontend():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("../frontend", path)

@app.route("/")
def home():
    return "Backend running clean da 🔥"

@app.route("/api/upload", methods=["POST"])
def upload_resume():
    file = request.files.get("resume")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = processor.extract_text_from_pdf(path)
    parsed = processor.parse_resume(text)

    overall, cats = calculate_scores(parsed)

    return jsonify({
        "overall_score": overall,
        "category_scores": cats,
        "parsed_data": parsed
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)
