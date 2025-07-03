from pydantic import BaseModel
from src.agents.tools import calculator
from src.infra.models import ChatResponse
from typing import Dict, Literal, Optional, Union
from langchain_core.output_parsers import PydanticOutputParser

class AgentAction(BaseModel):
    action: Literal["calculator", "normal_response", "follow_up_question"]
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Union[int, float, str]]] = None
    response: Optional[str] = None
    question: Optional[str] = None

parser = PydanticOutputParser(pydantic_object=AgentAction)

def get_response(parsed_response: str):
    print(f"Current response: {parsed_response}")

    if parsed_response.tool_name == "calculator" and parsed_response.tool_args:
        result = calculator.invoke(parsed_response.tool_args)
        return ChatResponse(response=str(result) if result else "Something went wrong.")

    elif parsed_response.action == "normal_response":
        return ChatResponse(response=parsed_response.response)

    elif parsed_response.action == "follow_up_question":
        return ChatResponse(response=parsed_response.question)
    
    return ChatResponse(response="Unrecognized action.")

