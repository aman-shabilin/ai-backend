import gradio as gr
import asyncio
from agents.agent import get_agent
from infra.models import ChatRequest

def chat_with_backend(message, history):
    try:
        request = ChatRequest(prompt=message)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_agent().chat(request.prompt))
        return result.response
    except Exception as e:
        return f"Error: {e}"

demo = gr.ChatInterface(fn=chat_with_backend, type="messages")
demo.launch()