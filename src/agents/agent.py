from typing import Literal, Optional
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Agent(BaseModel):
    action: Literal["use_tool","normal_response"] = Field(..., description="What the agent should do")
    tool_input: Optional[str]= Field(None, description="Arithmetic expression to send to calculator tool")
    response: Optional[str]= Field(None, description="Normal response if no tool is needed")

parser = PydanticOutputParser(pydantic_object=Agent)