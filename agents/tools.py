from langchain.tools import tool
from routers.pinecone import VectorStore
import re

vector_store = VectorStore()


@tool
def calculator(expression: str) -> str:
    """
    Use this tool to evaluate math expressions like '2 + 3'.
    Handles incomplete or malformed expressions and asks for clarification.
    """
    expression = expression.strip().replace("x", "*").replace("X", "*").replace("^", "**")

    if not re.fullmatch(r"[0-9\.\+\-\*/\(\)\s]+", expression):
        return "The expression contains invalid characters or symbols. Could you please rephrase it?"

    if re.search(r"[\+\-\*/]$", expression.rstrip()):
        return "It looks like the expression is incomplete. Could you please complete it?"

    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "I couldn't evaluate that expression. Could you double-check it?"
    
@tool    
def retrieve_tools(query: str) -> str:
    """
    Retrieve the list of products from vector store
    """
    try:
        res = vector_store.similarity_search(query)
        return res 
    except Exception as e:
        return f"Error retrieving products: {e}"


tools = [calculator, retrieve_tools]