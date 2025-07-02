from typing import Dict, Literal, Optional, Union
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser


class AgentAction(BaseModel):
    action: Literal["calculator", "normal_response", "follow_up_question"]
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Union[int, float, str]]] = None
    response: Optional[str] = None
    question: Optional[str] = None

parser = PydanticOutputParser(pydantic_object=AgentAction)
