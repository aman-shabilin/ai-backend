from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

class ChatGemini(): 

    def __init__(self, api_key:str):
        self.api_key = api_key
        self.model = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            google_api_key = api_key
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


