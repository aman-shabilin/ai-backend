import gradio as gr
import requests

API_URL = "http://localhost:8000/chat"  # Your FastAPI endpoint

def chat_with_api(message, chat_history):
    try:
        # Send prompt to FastAPI
        response = requests.post(API_URL, json={"prompt": message})
        bot_reply = response.json().get("response", "No response.")
    except Exception as e:
        bot_reply = f"Error: {str(e)}"
    
    chat_history.append((message, bot_reply))
    return "", chat_history  # Clear input, update history

with gr.Blocks(title="Blackbox AI Style Chat") as demo:
    gr.Markdown("<h2 style='text-align: center;'>🧠 Chat with Your AI Assistant</h2>")

    chatbot = gr.Chatbot(label="AI Chat", height=500)
    user_input = gr.Textbox(placeholder="Type your message here...", show_label=False, lines=3)

    submit_btn = gr.Button("Send", variant="primary")

    submit_btn.click(fn=chat_with_api, inputs=[user_input, chatbot], outputs=[user_input, chatbot])
    user_input.submit(fn=chat_with_api, inputs=[user_input, chatbot], outputs=[user_input, chatbot])

demo.launch()
