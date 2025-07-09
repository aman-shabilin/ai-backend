import gradio as gr
import asyncio
from agents.agent import get_agent
from infra.models import ChatRequest, ChatResponse

def chat_with_backend(message, history):
    try:
        result = get_agent().chat(message)  # result is a string
        chatresponse = ChatResponse(response=result)
        return chatresponse.response  # ✅ this works
    except Exception as e:
        return f"Error: {e}"

demo = gr.ChatInterface(fn=chat_with_backend, type="messages")
demo.launch()