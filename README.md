# 🤖 AI Student Resume Analyser

A web-based resume analysis application built with Python and Flask. It extracts information from student resumes, evaluates important sections, and generates an overall resume score with category-wise results.

## 📌 Project Overview

The AI Student Resume Analyser aims to help students understand the quality and structure of their resumes.

Users can upload a PDF resume through a web interface. The Python backend extracts resume text, identifies relevant information, and evaluates the resume using predefined rules and scoring criteria.

## ✨ Features

- 📄 Upload resumes through a web interface.
- 🔍 Extract text from PDF documents.
- 🎓 Identify education details.
- 💼 Detect work experience and projects.
- 🛠️ Identify technical and soft skills.
- 📊 Calculate overall resume scores.
- 📈 Display category-wise scores.
- 📧 Extract contact information such as email and phone number.
- 📋 Display structured resume analysis results.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Backend web framework and REST API |
| PyPDF2 | PDF text extraction |
| HTML5 | Frontend structure |
| CSS3 | Frontend styling |
| JavaScript | Frontend interactions and API communication |
| Git | Version control |
| GitHub | Source code management |
| MySQL Connector | Database connectivity component |

## 🏗️ Application Architecture

The application follows a simple frontend-backend architecture.

```text
             User
               |
               v
       Web Browser
               |
               v
       HTML / CSS / JS
               |
               | HTTP Request
               v
         Flask Backend
               |
               v
        Resume Processor
               |
               v
       PDF Text Extraction
               |
               v
       Resume Parsing
               |
               v
        Scoring Logic
               |
               v
       JSON API Response
               |
               v
       Analysis Dashboard
```

## 📂 Project Structure

```text
AI-StudentResumeAnalyser/
│
├── app.py
├── main_app.py
├── config.py
├── database.py
├── resume_engine.py
├── scoring.py
├── scoring_engine.py
├── utils.py
│
├── index.html
├── styles.css
├── script.js
│
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Prerequisites

Before running the application, install:

- Python 3.x
- pip (Python package manager)
- Git
- VS Code or another code editor
- A modern web browser

## 🚀 Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

### Step 2: Navigate to the project directory

```bash
cd AI-StudentResumeAnalyser
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / Ubuntu:**

```bash
source venv/bin/activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Start the Flask backend

```bash
python app.py
```

The backend runs at:

```text
http://127.0.0.1:5000
```

### Step 7: Start the frontend

Open another terminal in the project directory and run:

```bash
python -m http.server 5500
```

Open the application in your browser:

```text
http://127.0.0.1:5500/index.html
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check backend availability |
| POST | `/api/upload` | Upload and analyse a resume |

### Resume Upload API

The application accepts a resume through a multipart form-data request.

**Request field:**

```text
resume: PDF file
```

**Response includes:**

- Overall resume score
- Category-wise scores
- Extracted resume information
- Parsed resume data

## 📊 Resume Evaluation

The current scoring implementation evaluates the following categories:

- Formatting
- Content
- Experience
- Skills

The backend calculates scores using predefined rules and resume content.

## 🔒 Security Considerations

- Do not commit API keys, passwords or sensitive credentials.
- Keep environment-specific configuration outside public repositories.
- Avoid uploading confidential or personal resumes when testing a public deployment.
- Configure secure file handling before production deployment.

## 🔮 Future Enhancements

- Integrate AI/LLM-based resume analysis.
- Improve resume parsing accuracy.
- Add personalized improvement recommendations.
- Implement ATS keyword matching.
- Integrate database-backed resume history.
- Improve upload validation and security.
- Containerize the application using Docker.
- Implement CI/CD automation.
- Explore AWS cloud deployment.

## 👨‍💻 Author

**Karthick Raja R**

- GitHub: https://github.com/karthick61201
- LinkedIn: https://www.linkedin.com/in/karthick-raja-r-204654213/

---

⭐ If you find this project interesting, feel free to explore the repository!

*Learning continuously. Building practically. Exploring new technologies.*
