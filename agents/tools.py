from langchain.tools import tool
from typing import Callable
import re

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
    
def make_retrieve_tool(qa_chain) -> Callable:
    @tool
    def retrieve_tools(query: str) -> str:
        """
        Retrieve the list of products from the vector store.
        """
        return qa_chain.invoke(query)
    
    return retrieve_tools
