import os
import google.generativeai as genai
from typing import List, Optional
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.chains import ConversationChain
from pydantic import Field

def load_system_prompt():
    with open("src/prompt/system_prompt.md", "r") as f:
        return f.read()

system_prompt_text = load_system_prompt()

system_prompt = SystemMessagePromptTemplate.from_template(system_prompt_text)
human_prompt = HumanMessagePromptTemplate.from_template("{text}")

chat_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    human_prompt
])

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    ValueError("GEMINI_API_KEY environment variable is not set")



class ChatGemini(BaseChatModel): 
    api_key :str
    model : str = "gemini-2.0-flash"
    system_prompt: Optional[str] = None
    model: genai.GenerativeModel = Field(default=None, exclude=True)

    model: Optional[genai.GenerativeModel] = Field(default=None, exclude=True)

    def __init__(self, **data):
        api_key = data.get("api_key")
        model_name = data.get("model", "gemini-2.0-flash")

        genai.configure(api_key=api_key)
        data["model"] = genai.GenerativeModel(model_name)

        super().__init__(**data)

    @property
    def _llm_type(self) -> str:
        return "chat-gemini"

    def _generate(self, messages: List[BaseMessage], stop=None) -> ChatResult:
        history = []

        if self.system_prompt:
            history.append(SystemMessage(content=self.system_prompt))

        history += messages

        def convert_message(m: BaseMessage):
            if m.type == "human":
                return {"role": "user", "parts": [m.content]}
            elif m.type == "ai":
                return {"role": "model", "parts": [m.content]}
            elif m.type == "system":
                return {"role": "user", "parts": [f"[SYSTEM INSTRUCTION]: {m.content}"]}
            else:
                raise ValueError(f"Unsupported message type: {m.type}")

        chat = self._model.start_chat(
            history=[convert_message(m) for m in history]
        )

        last_user_msg = [m for m in messages if isinstance(m, HumanMessage)][-1].content
        response = chat.send_message(last_user_msg)

        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=response.text))])
    
llm = ChatGemini(api_key=gemini_api_key, model="gemini-2.0-flash", system_prompt=system_prompt_text)

chat_chain = ConversationChain(
    llm=llm,
    memory=memory,
    input_key="text",
    verbose=True
)
