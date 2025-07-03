from typing import Annotated
from langchain.tools import tool
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression like '1+1'."""
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Invalid expression: {e}"