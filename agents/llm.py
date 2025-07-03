from .chat import LLM
from agents.tools import tools
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
        
class ChatGemini(LLM): 

    def __init__(self, api_key:str, system_prompt: str = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.model = ChatGoogleGenerativeAI(
            model = "gemini-2.0-flash",
            google_api_key = api_key
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = initialize_agent(
            tools=tools,
            llm=self.model,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True  # helpful for dev
        )
    def chat(self, prompt: str) -> str:
        try: 
            result = self.agent.run(prompt)
            return result
        except Exception as e:
            return f"Agent error: {e}"
