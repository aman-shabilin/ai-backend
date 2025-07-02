import os 
from fastapi import FastAPI
from .agents.agent import parser
from .agents.tools import calculator
from .prompt.prompt import SYSTEM_PROMPT
from fastapi.middleware.cors import CORSMiddleware
from .infra.models import ChatResponse, ChatRequest
from .agents.llm import ChatGemini, gemini_api_key, prompt_template, memory

app = FastAPI()

model = ChatGemini(api_key=gemini_api_key, system_prompt=SYSTEM_PROMPT)

origins=[
    "https://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):

    formatted_prompt = prompt_template.format(
        request = request.prompt,
        format_instructions = parser.get_format_instructions()
    )

    response = model.chat(prompt=formatted_prompt)

    parsed_response = parser.parse(response.content)
    print(f"Current response: {parsed_response}")
    # return ChatResponse(response=parsed_response.response)
    if parsed_response.action == "use_tool":
        if parsed_response.tool_name == "calculator" and parsed_response.tool_args:
            result = calculator(**parsed_response.tool_args)
            return ChatResponse(response=str(result))
        else:
            return ChatResponse(response="Tool not supported or missing arguments.")
        
    elif parsed_response.action == "normal_response":
        # memory.chat_memory.add_user_message(request.prompt)
        # memory.chat_memory.add_ai_message(parsed_response.response)
        return ChatResponse(response=parsed_response.response)
    
    elif parsed_response.action == "follow_up_question":
        # memory.chat_memory.add_user_message(request.prompt)
        # memory.chat_memory.add_ai_message(parsed_response.question)
        return ChatResponse(response=parsed_response.question)
        
@app.get("/")
async def root(): 
    return {"message": "API is running"}
