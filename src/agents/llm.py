import os
from dotenv import load_dotenv
from .chat import LLM
from src.prompt.prompt import SYSTEM_PROMPT
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")

if not gemini_api_key:
    ValueError("GOOGLE_API_KEY environment variable is not set")
        
memory = ConversationBufferMemory(k=3, return_messages=True)

prompt_template = PromptTemplate.from_template(SYSTEM_PROMPT)

class ChatGemini(LLM): 
    def __init__(self, api_key:str, system_prompt: str = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.model = ChatGoogleGenerativeAI(
            model = "gemini-2.0-flash",
            google_api_key = gemini_api_key
        )
    def chat(self, prompt: str) -> str:
        chat_history = memory.chat_memory.messages.copy()

        if not any(isinstance(m, SystemMessage) for m in chat_history):
            chat_history.insert(0, SystemMessage(content=SYSTEM_PROMPT))
        
        chat_history.append(HumanMessage(content=prompt))
        response = self.model.invoke(chat_history)
        memory.chat_memory.add_user_message(prompt)
        memory.chat_memory.add_ai_message(response)

        return response
