from langchain.tools import tool
import requests
@tool
def calculator(expression: str) -> str:
    """
    Call external calculator API to evaluate an arithmetic expression.

    Args:
        expression: A string like "3 + 5"
    """
    try:
        response = requests.post(
            "http://localhost:8000/api/calculate",  # or your actual endpoint
            json={"expression": expression}
        )
        result = response.json().get("result")
        return str(result)
    except Exception as e:
        return f"Calculator error: {str(e)}"
    
tools = [calculator]