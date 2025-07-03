🔧 Setup Instructions
1. Clone the Repository

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create & Activate Virtual Environment

# Create a virtual environment
python -m venv venv

# Activate it (use one of these depending on OS)
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install Required Packages

pip install -r requirements.txt

🚀 Run the Application
1. Start the Backend (FastAPI)

uvicorn src.main:app --reload

This will start your backend at:
📍 http://localhost:8000
2. Start the Chatbot Frontend

In another terminal, while the backend is running:

python frontend.py

This will launch a Gradio-based chat interface in your browser (e.g. http://127.0.0.1:7860).
💬 Features

    Chat history (like Blackbox AI or ChatGPT)

    Large prompt box + streaming-style response (optional)

    Extendable with memory, tools, or structured agents

📁 Project Structure

├── frontend.py           # Gradio chat interface
├── requirements.txt      # Python dependencies
├── src/
│   └── main.py           # FastAPI app entry point
├── prompt_formatter.py   # (optional) Prompt formatting util
└── README.md             # You’re here!

🛠 To Do

Add streaming support

Save chat history to file

Deploy to Hugging Face or Docker
