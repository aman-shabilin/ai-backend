from .chat import LLM
from agents.tools import tools
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent


class ChatGemini(LLM): 

    def __init__(self, api_key:str):
        self.api_key = api_key
        self.model = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            google_api_key = api_key
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        sys_msg = """Assistant is a large language model trained by OpenAI.

        Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

        Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

        Unfortunately, Assistant is terrible at maths. When provided with math questions, no matter how simple, assistant always refers to it's trusty tools and absolutely does NOT try to answer math questions by itself. Then, it try to calculate even with malformed expression or incomplete expression.

        Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
        """
        self.agent = initialize_agent(
            tools=tools,
            llm=self.model,
            agent='chat-conversational-react-description',
            memory=self.memory,
            verbose=True  # helpful for dev
        )

        new_prompt = self.agent.agent.create_prompt(
            system_message = sys_msg,
            tools = tools
        )
        self.agent.agent.llm_chain.prompt = new_prompt

    def chat(self, prompt: str) -> str:
        try: 
            result = self.agent.run(prompt)
            return result
        except Exception as e:
            return f"Agent error: {e}"

