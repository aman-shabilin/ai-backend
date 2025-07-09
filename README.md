---
title: ai-backend
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

# 🧱 Architecture Overview
This project integrates two main AI functionalities:

## 1. Retrieval-Augmented Generation (RAG)
Purpose: Answers natural language queries based on product data.

Flow:

🗣️ User query → 🧠 Embedding (BAAI/bge-small-en-v1.5) → 📦 Pinecone search → 🤖 LLM generates answer using relevant data.
Used for: /products endpoint.

## 2. 📊 Text-to-SQL (Text2SQL)
Purpose: Converts natural language queries into SQL to query outlet data.

Flow:

🗣️ Query → 🧾 Schema-aware prompt → 🧠 LLM → 🗃️ SQL generation → 🏁 Query execution → 📤 Result returned.

Used for: /outlets endpoint.

# ⚖️ Key Trade-offs

| 📌 Area             | ✅ Decision               | ⚠️ Trade-off                                                                  |
| ------------------- | ------------------------ | ----------------------------------------------------------------------------- |
| **Embedding Model** | `BAAI/bge-small-en-v1.5` | Small and efficient, but may miss subtle context.                             |
| **Vector Store**    | Pinecone                 | Fast and scalable, but requires external setup and usage limits on free tier. |
| **UI Framework**    | Gradio                   | Quick to integrate, but limited design flexibility.                           |
| **Model Strategy**  | Pre-trained LLMs only    | No fine-tuning needed, but domain-specific accuracy may vary.                 |
| **Framework**       | FastAPI + LangChain      | Clean modularity and future-proofing, but learning curve for newcomers.       |
