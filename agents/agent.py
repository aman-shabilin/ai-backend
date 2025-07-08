import os
from .chat import LLM
from dotenv import load_dotenv
from agents.llm import ChatGemini
from agents.tools import calculator
from langchain_core.tools import Tool
from routers.pinecone import VectorStore
from langchain.chains.question_answering import load_qa_chain
from langchain.agents import initialize_agent

load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")

vector_store = VectorStore()
llm = ChatGemini(api_key=gemini_api_key)


qa_chain = load_qa_chain(llm.model, chain_type="stuff")

def ask_product_query(query: str) -> str:
    product_search = vector_store.retrieve(query, k=5)
    result = qa_chain.invoke({
        "input_documents": product_search,
        "question": query
    })
    return result


retriever_tool = Tool.from_function(
    name="ProductRetriever",
    func=ask_product_query,
    description="Useful for answering product-related questions using the ZUS vector store.",
)

tools = [
    calculator,
    retriever_tool
]

class get_agent(LLM):
        def __init__(self):
            sys_msg = """Assistant is a large language model trained by OpenAI.

            Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

            Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

            Unfortunately, Assistant is terrible at maths. When provided with math questions, no matter how simple, assistant always refers to it's trusty tools and absolutely does NOT try to answer math questions by itself. Then, it try to calculate even with malformed expression or incomplete expression.

            Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
            """
            self.agent = initialize_agent(
                tools=tools,
                llm=llm.model,
                agent='chat-conversational-react-description',
                memory=llm.memory,
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