import gradio as gr
import requests


def chat_with_backend(messages, history):
    print(f"Message : {messages}")
    try:
        res = requests.post(
            "http://localhost:8000/chat",
            json={"prompt": messages},
        )
        return res.json()["response"]
    except Exception as e:
        return f"Error: {e}"
        

demo = gr.ChatInterface(fn=chat_with_backend, type="messages")
demo.launch(server_name="0.0.0.0", server_port=7860)
