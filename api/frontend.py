import gradio as gr
from agents.agent import get_agent
from infra.models import ChatResponse

def chat_with_backend(message, history):
    try:
        result = get_agent().chat(message)
        chatresponse = ChatResponse(response=result)
        return chatresponse.response  
    except Exception as e:
        return f"Error: {e}"

demo = gr.ChatInterface(fn=chat_with_backend, type="messages")
demo.launch()