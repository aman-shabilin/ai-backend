import os
from .chat import LLM
from agents.llm import ChatGemini
from agents.tools import calculator
from langchain_core.tools import Tool
from routers.pinecone import VectorStore
from langchain.agents import initialize_agent
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.question_answering import load_qa_chain
from langchain_core.runnables import RunnablePassthrough , RunnableLambda, RunnableMap, RunnableBranch
from routers.db import db, run_query, clean_sql_output,nl_response_prompt, sql_prompt, intent_prompt

#Import the Pinecone vector store
vector_store = VectorStore()

# Gemini api key from .env file
gemini_api_key = os.getenv("GOOGLE_API_KEY")

#Import llm model from the ChatGemini class
llm = ChatGemini(api_key=gemini_api_key)


def ask_product_query(query: str) -> str:
    qa_chain = load_qa_chain(llm.model, chain_type="stuff")
    product_search = vector_store.retrieve(query, k=1)

    if not product_search:
        return "Sorry, I couldn't find any product information related to your query."

    result = qa_chain.invoke({
        "input_documents": product_search,
        "question": query
    })

    return result.get("output_text") or result.get("answer") or "Sorry, no summary could be generated."


def ask_outlet_query(query: str) -> str:

    intent_check_chain = intent_prompt | llm.model | StrOutputParser()

    sql_chain = (RunnablePassthrough.assign(schema=lambda _: db.get_table_info()
                                        )
            | sql_prompt
            | llm.model.bind(stop=["\n SQLResult: "])
            | StrOutputParser()
            | RunnableLambda(clean_sql_output)
            )

    full_chain = (
        RunnableMap ({
            "intent": lambda vars: vars["question"],
            "question": lambda vars: vars["question"]
        })
        |
        RunnableBranch(
        # Case 1: Not clear (No)
        (lambda vars: vars["intent"].strip().lower().startswith("no"),
         RunnableLambda(lambda _: "Please clarify your question with a specific location or service type (e.g. 'Any outlets in Shah Alam?').")),
        # Case 2: Clear (Yes)
        RunnablePassthrough.assign(query=sql_chain).assign(
        schema=lambda _: db.get_table_info(),
        response=lambda vars: run_query(vars["query"]),)
            )
            | nl_response_prompt
            | llm.model
            | RunnableLambda (lambda msg: msg.content)
    )
    
    result = full_chain.invoke({"question": query})
    return result

retriever_tool = Tool.from_function(
    name="ProductRetriever",
    func=ask_product_query,
    description="Useful for answering product-related questions using the ZUS vector store.",
)

sql_tool = Tool.from_function(
    name="OutletRetriever",
    func=ask_outlet_query,
    description="Useful for finding ZUS outlet name, address, services or opening/closing hours from the database.",
)

tools = [
    calculator,
    sql_tool,
    retriever_tool
]

# Create a custom agent class to execute an action whether to ask follow up question, execute a tool, or retrieve data from vector store or SQL database.
class get_agent(LLM):
        def __init__(self):
            sys_msg = """
            Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
            Assistant will decide which tool to use based on the input it receives. It has access to a variety of tools, including a calculator for performing mathematical calculations, a SQL database for answering questions about ZUS outlets, and a vector store for retrieving information about ZUS drinkware products. If the input is vague or ambiguous, Assistant will clarify the question before proceeding with the task.

            Unfortunately, Assistant is terrible at maths. When provided with math questions, no matter how simple, assistant always refers to it's trusty tools and absolutely does NOT try to answer math questions by itself. Then, it try to calculate even with malformed expression or incomplete expression.
            You have access to:
            1. A product search tool that can answer questions about tumblers, cups, mugs, etc.
            2. An outlet search tool that can find store locations and services.

            You MUST use prior conversation context to resolve follow-up questions. For example:
            - If the user asks “where can I get it?” after asking about a blue tumbler, you should combine this context.
            - If they mention a location like “PJ” or “KL”, you must use the outlet search tool.
            - First must parses the intent of the user question then decide which action should be taken.

            You are expected to reason step-by-step before deciding which tool to call.
            Ask clarifying questions when needed, and prefer to guide the user helpfully.            """
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