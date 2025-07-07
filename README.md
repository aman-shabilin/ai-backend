---
title: ai-chatbot
app_file: ./api/frontend.py
sdk: gradio
sdk_version: 5.35.0
---
# 🧠 AI Chatbot (Backend + Frontend)

A simple Python chatbot interface inspired by Blackbox AI, built using FastAPI and Gradio.

---

## 📦 Requirements

- Python 3.8+
- `pip`, `venv`

---

# 🔧 Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```


## 2. Create & Activate Virtual Environment

Create a virtual environment
```
python -m venv venv
```

Then, activate the virtual environment

### On Windows
```
venv\Scripts\activate
```
### On macOS/Linux
```
source venv/bin/activate
```

## 3. Install Dependencies
```
pip install -r requirements.txt
```

# 🚀 Run the Application
## 1. Start the Backend (FastAPI)
```
uvicorn src.main:app --reload
```
Backend will start at: http://localhost:8000
## 2. Start the Chatbot Frontend (Gradio)

In another terminal (with the same virtual environment activated):
```
python frontend.py
```
This will launch a Gradio chat interface in your browser:
👉 http://127.0.0.1:7860



