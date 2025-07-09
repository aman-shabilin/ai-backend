import gradio as gr
import asyncio
from agents.chat import chat
from agents.agent import get_agent
from infra.models import ChatRequest


def chat_with_backend(messages, history):
    try:
        request = ChatRequest(prompt=messages)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_agent.chat(request))
        return result.response
    except Exception as e:
        return f"Error: {e}"


demo = gr.ChatInterface(fn=chat_with_backend, type="messages")
demo.launch()
